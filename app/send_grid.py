"""
test1-
3
service u1
add u1 michelle 1
add u1 jose 2

out1
service u1
michelle 1
jose 2

test2-
3
service u1
add u1 mary 1
add u1 mary 1

out2 -
service u1
mary 1

test3-
3
service s1
add s1 mary 1
delete s1 mary 1

out3-
service s1

test4-
3
service s1
add s1 mary 1
add s1 joe 1

out4-
service s1
joe 1

test5-
6
service s1
add s1 joe 1
service s2
add s2 jane 2
register s1 s2
add s1 jack 3

out5-
service s1
joe 1
jack 3
service s2
jane 2
jack 3

test 6-
8
service s1
add s1 mary 1
add s1 joe 2
service s2
add s2 mary 1
add s2 joe 3
register s1 s2
delete s1 mary 1

out6-
service s1
joe 2
service s2
joe 3

test 7-
6
service s1
service s2
register s1 s2
register s2 s1
add s1 tina 1
add s2 tom 2

out7-
service s1
tina 1
tom 2
service s2
tina 1
tom 2

test8-
8
service s1
service s2
register s1 s2
register s2 s1
add s1 tina 1
add s2 tom 2
deregister s1 s2
add s1 george 1

out8-
service s1
george 1
tom 2
service s2
tina 1
tom 2

test9-
8
service u1
add u1 michelle 1
add u1 jose 2
add u1 jack 5

"""


class User(object):
    def __init__(self, name, uid):
        pass


class UserService(object):
    def __init__(self, name):
        pass

    def add_user(self, user):
        pass

    def delete_user(self, user):
        pass

    def get_users(self):
        pass

    def register_listener(self, service):
        pass

    def deregister_listener(self, service):
        pass

if __name__ == '__main__':
    services = []
    lookup = {}
    commands = int(input())
    for c in range(0, commands):
        command = input().split()
        if command[0] == 'add':
            serviceName = command[1]
            s = lookup[serviceName]
            s.add_user(User(command[2], command[3]))
        elif command[0] == "delete":
            serviceName = command[1]
            s = lookup[serviceName]
            s.delete_user(User(command[2], command[3]))
        elif command[0] == 'service':
            serviceName = command[1]
            s = UserService(serviceName)
            services.append(s)
            lookup[serviceName] = s
        elif command[0] == 'register':
            s1 = lookup[command[1]]
            s2 = lookup[command[2]]
            s1.register_listener(s2)
        elif command[0] == 'deregister':
            s1 = lookup[command[1]]
            s2 = lookup[command[2]]
            s1.deregister_listener(s2)
    for service in services:
        print(service)
        for user in service.get_users():
            print(user)
