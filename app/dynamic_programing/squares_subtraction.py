"""
Given invariant: Start with a non-negative positive integer X and 2 players.
Each player subtracts a perfect square from X. The game ends when X = 0
They take alternate turns and play

We are assuming that we subtract a perfect square any number of times.
Clarify that assumption.

3 parts to an interview
1) Understanding the problem with use cases and asking clarifying questions
2) Algorithm formulation
3) Fluency of coding the solution

Tip: Dont ask the interviewer to validate your hypothesis.
You have to validate your own hypothesis by talking aloud to yourself introspectively,
and using examples.

Approach for DP problems:
1) Recognize that its a dynamic programing problem
2) Identify the recursive step & define sub-problems
3) What are the base cases?
4) Memoization
"""


def get_optimal_move(curr_state):
    if mem[curr_state].exists():
        return mem[curr_state]
    for i in range(1, int(sqrt(curr_state)) + 1):
        if get_optimal_move(curr_state - i * i) is None:
            return i*i
    return None
    pass


if __name__ == '__main__':
    print get_optimal_move(151)
