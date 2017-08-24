"""
detect a cycle in a linked list

service unavailability if there is an infinite loop

in a rest api like service, you request for more records, it keeps giving you the same records
over and over again.

have 2 pointers, 1 faster, another slower. If they meet, there is a cycle (constant memory)

Another approach is to use a hashset for all visited nodes (linear extra space)
"""