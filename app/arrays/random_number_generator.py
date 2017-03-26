"""
Give G3 and G5, how to generate G20?

where G3 = random numbers from 1 to 3
G5 = random numbers from 1 to 5
G20 = uniform selection of random numbers from 1 to 20

Hint: Its a trick question. If you are writing code, you're doing the wrong thing.
Its impossible to do this in theory. If you execute G3 n times and G5 m times,
you get 3^n * 5^m possible executions for each outcome.

There should be 20 possible outcomes from the executions, ie a number from 1 to 20.

But (3^n * 5^m)/20 does not divide as the number of prime factors dont divide.
(3^n * 5^m)/(2*2*5)

What can we do if the interviewer insists that you can?
Program should implement the following hard-coded table
   1  2  3
1  1  2  3
2  4  5  6
3  7  8  9
4 10 11 12
5 13 14 15
6 16 17 18
7 19 20 try_again

Running time of algorithm is unbounded.
Compare the number of executions to the number of outcomes and just by comparing these 2 numbers,
you will have solid talking points.
"""