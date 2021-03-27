# https://gist.github.com/ChimeraCoder/1906326162eb88742952
# https://gist.github.com/antifuchs/dd5344b60693dd1d073b

# next_server_number([5, 3, 1])
#  2
#  >> next_server_number([5, 4, 1, 2])
#  3
#  >> next_server_number([3, 2, 1])
#  4
#  >> next_server_number([2, 3])
#  1
#  >> next_server_number([])
#  1

# Write a name tracking class with two operations, allocate(host_type) and deallocate(hostname).
# The former should reserve and return the next available hostname, while the latter should release
# that hostname back into the pool.

# >> tracker = Tracker.new()
# >> tracker.allocate("apibox")
# "apibox1"
# >> tracker.allocate("apibox")
# "apibox2"
# >> tracker.deallocate("apibox1")
# nil
# >> tracker.allocate("apibox")
# "apibox1"
# >> tracker.allocate("sitebox")
# "sitebox1"


class Tracker(object):
    def __init__(self):
        self.map = {}

    def allocate(self, s):
        if s in self.map:
            val_arr = self.map[s]
            next_server = self.next_server_number(val_arr)
            val_arr.append(next_server)
            self.map[s] = val_arr
        else:
            next_server = self.next_server_number([])
            self.map[s] = [next_server]
        return s + str(next_server)

    def deallocate(self, s):
        # split s into str and integer portions

        for i, c in enumerate(s):
            if not 49 <= ord(c) <= 57:
                continue
            else:
                int_start_index = i
                break

        server_to_dealloc = s[int_start_index:]
        server = s[:int_start_index]
        if server in self.map:
            val_arr = self.map[server]
            try:
                val_arr.remove(int(server_to_dealloc))
                self.map[server] = val_arr
            except ValueError:
                return None
        else:
            return None

    def next_server_number(self, a):
        if a is None:
            return None
        st = set()
        for e in a:
            st.add(e)

        for i in range(1, len(a) + 2):
            if i not in st:
                return i


if __name__ == '__main__':
    tracker = Tracker()
    print(tracker.allocate("apibox"))
    print(tracker.allocate("apibox"))
    print(tracker.deallocate("apibox1"))
    print(tracker.allocate("apibox"))
    print(tracker.allocate("sitebox"))

    # print next_server_number([5, 3, 1])  # 2
    # print next_server_number([5, 4, 1, 2]) # 3
    # print next_server_number([3, 2, 1]) # 4
    # print next_server_number([2, 3]) # 1
    # print next_server_number([]) # 1
