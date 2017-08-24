"""
Given a phone keypad like below -
1 2 3
4 5 6
7 8 9
  0

How many different 10-digit numbers can be formed starting from 1 such that the movement from
1 digit to the next is similar to a Knight on a chess board?

eg - 1616161616 is a valid number, repetitions are allowed.

Just give the count of 10-digit numbers and not necessarily the list of numbers.
Find a polynomial-time solution based on dynamic programing.

Reference -
http://stackoverflow.com/questions/2893470/generate-10-digit-number-using-a-phone-keypad

Python implementation -
https://github.com/harishvc/challenges/blob/master/dp-knight-chess-movement.py
"""