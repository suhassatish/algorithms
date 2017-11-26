import ipdb
from collections import deque

DEFINED_COMMANDS = ['DEPEND', 'INSTALL', 'REMOVE', 'LIST', 'END']


class DependencyManager(object):

    def __init__(self):
        self.component_dependencies_map = dict()  # key = component and values = set of components it depends on

        self.component_used_by_map = dict()  # inverse map of `component_dependencies_map`;
        # key = base component and values = set of components that are using the
        #  base component
        self.installed = set()

    def depend(self, item_list):
        """

        :param item_list: takes a list of items after the DEPEND keyword and updates the 2 internal maps accordingly
        item_list should be of atleast length 2, otherwise its an invalid command and raises a warning
        :return: None
        """
        if item_list is None or len(item_list) < 2:
            raise SyntaxWarning("DEPEND should be followed by atleast 2 words. If not, its redundant")
        primary_component = item_list[0]
        dependencies = item_list[1:]

        inverse_dependency_exists = self._check_if_inverse_dependency_exists(primary_component, dependencies)

        if not inverse_dependency_exists:
            if primary_component not in self.component_dependencies_map:
                self.component_dependencies_map[primary_component] = set(dependencies)

                # now add the inverse dependency
                self._update_component_used_by_map(primary_component, dependencies)

            else:
                existing_dependencies = self.component_dependencies_map[primary_component]
                for new_dependency in dependencies:
                    existing_dependencies.add(new_dependency)
                self.component_dependencies_map[primary_component] = existing_dependencies

                # now add the inverse dependency
                self._update_component_used_by_map(primary_component, dependencies)

    def install(self, item):
        """
        Installs all the items that item depends on
        :param item: It is a list of items to install
        :return:
        """
        if item is None or (isinstance(item, list) and len(item) > 1):
            raise SyntaxError("Only 1 component has to be specified with INSTALL per line")

        item = item[0]
        if item in self.installed:
            print("{} is already installed".format(item))
            return

        if item not in self.component_dependencies_map:
            # it is a base_component not already installed, and which doesnt need any pre-requisites
            self._install(item)

        else:
            # item has dependencies. Traverse the dependency list to the base component and install them in
            # topologically sorted order
            install_order = []
            connected_components = self._find_connected_components(item)
            visited_set = set()
            for component in connected_components:
                if component not in visited_set:
                    self._topological_sort(item, install_order, visited_set)

            for dep in install_order:
                self._install(dep)

    def remove(self, item):
        """
        Remove item1 and those on which it depends, if possible
        :param item:
        :return:
        """
        if item is None or (isinstance(item, list) and len(item) > 1):
            raise SyntaxError("Only 1 component has to be specified with REMOVE per line")
        item = item[0]
        if item not in self.installed:
            print("{} is not installed".format(item))
            return

        if not self._can_remove(item):
            print("{} is still needed".format(item))
            return

        # remove component and other connected components if they're no longer used
        connected_components = self._find_connected_components(item)
        remove_order = []
        visited_set = set()
        for component in connected_components:
            if component not in visited_set:
                self._topological_sort(item, remove_order, visited_set)
        remove_order.reverse()

        for dep in remove_order:
            self._remove(dep)

            # item has dependencies. Traverse the dependency list to the base component and install them in
            # topologically sorted order

    def list(self):
        """
        List the names of all currently-installed components
        :return:
        """
        for item in self.installed:
            print(item)

    def _check_if_inverse_dependency_exists(self, primary_component, dependencies):
        for dependency in dependencies:
            try:
                current_set = self.component_used_by_map[primary_component]
                if dependency in current_set:
                    print("{} depends on {}, ignoring command".format(dependency, primary_component))
                    return True
            except KeyError:
                continue

        return False

    def _update_component_used_by_map(self, primary_component, dependencies):
        """
        :param primary_component:
        :param dependencies: is a list of dependencies
        :return:
        """
        for dependency in dependencies:
            if dependency not in self.component_used_by_map:
                new_set = set()
                new_set.add(primary_component)
                self.component_used_by_map[dependency] = new_set
            else:
                used_by_set = self.component_used_by_map[dependency]
                used_by_set.add(primary_component)
                self.component_used_by_map[dependency] = used_by_set

    def _install(self, item):
        """
        Helper private method for install
        :param item:
        :return:
        """
        if item not in self.installed:
            self.installed.add(item)
            print("Installing {}".format(item))

    def _remove(self, item):
        """
        Helper private method for remove
        :param item:
        :return:
        """
        if self._can_remove(item):
            self.installed.remove(item)
            print("Removing {}".format(item))

    def _can_remove(self, item):
        try:
            item_used_by_set = self.component_used_by_map[item]
        except KeyError:
            item_used_by_set = set()

        if len(self.installed.intersection(item_used_by_set)) > 0:
            return False
        else:
            return True

    def _topological_sort(self, item, stk, visited_set):
        """
        stk should be an empty list
        Returns topologically sorted order in which dependencies should be installed
        :return: stk which is the topologically sorted install order of connected components
        """
        visited_set.add(item)
        for u in self._adj(item):
            if u not in visited_set:
                self._topological_sort(u, stk, visited_set)

        stk.append(item)

    def _find_connected_components(self, item):
        """
        Traverse the dependency map from current item upto all its prerequisites
        and return a set of connected components
        :param item:
        :return: set of connected components
        """
        out = set()
        q = deque()
        q.append(item)
        out.add(item)
        while q:
            v = q.popleft()
            for u in self._adj(v):
                q.append(u)
                out.add(u)
        return out

    def _adj(self, item):
        """
        Returns the adjacent elements in the directed graph of components connected
        up to their pre-requisite dependency components
        :param item:
        :return:
        """
        if item in self.component_dependencies_map:
            return self.component_dependencies_map[item]
        else:
            return set()

    def end(self):
        pass


class DependencyManagerClient(object):
    def parse_file(self, full_file_path_with_filename):
        """

        :param full_file_path_with_filename: eg - /Users/ssatish/git/algorithms/sample_input.txt
        :return:
        """
        dm = DependencyManager()
        with open(full_file_path_with_filename, 'r') as f:
            cmd_count = int(f.readline())
            for _ in range(cmd_count):
                line = f.readline()
                words = line.split()
                command = words[0]
                if command not in DEFINED_COMMANDS:
                    raise SyntaxError("Command {} not supported. Supported commands: {}".format(command, DEFINED_COMMANDS))

                print(line)
                if command == 'DEPEND':
                    dm.depend(words[1:])
                if command == 'INSTALL':
                    dm.install(words[1:])
                if command == 'REMOVE':
                    dm.remove(words[1:])
                if command == 'LIST':
                    dm.list()
                if command == 'END':
                    dm.end()


def main():
    dmc = DependencyManagerClient()
    dmc.parse_file("sample_input.txt")  # assumes the current python file and the sample_input are in the same package


if __name__ == '__main__':
    main()
