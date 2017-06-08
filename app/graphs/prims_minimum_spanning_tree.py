"""
https://www.youtube.com/watch?v=dVvr9RC5HHc
Princeton algorithms illustration demo video

Application: Repairs roads with minimum cost. What roads to repair?

1) Start with vertex 0 and greedily grow tree T
2) Add to T the min_wt_edge with exactly 1 endpoint in T
3) Repeat until V - 1 edges

"""