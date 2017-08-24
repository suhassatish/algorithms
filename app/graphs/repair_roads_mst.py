"""
Houses in a city connected by roads. (like a graph)
Repair some roads such that each house can reach every other house without hitting a pot hole.
AND
Minimize the total cost of road repairs.

ie, you don't want to repair everything.

This is a Prim's minimum_spanning_tree (MST) problem

Given houses A, B, C, D, E, F represented as nodes on a graph with edges representing
roads, and edge_weights representing number of pot holes on each road.

A - B (2)
A - C (5)
B - C (8)
B - F (9)
F - E (3)
C - D (11)
F - C (6)

Kruskal's algorithm is good for clustering, when k is known. This question was asked at Palantir

"""