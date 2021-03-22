"""
Asked in Facebook onsite interview in June 2017

Given a string S and a string T, find the minimum window in S which contains all the characters in T.
For example, S = "AYZABOBECODXBANC" and T = "ABC", min window is "BANC" which contains all letters A, B and C.

If no such window exists, return empty string.
If there are multiple minimum windows, return any one.
Characters may be repeated (duplicate letters).

https://discuss.leetcode.com/topic/20692/12-lines-python


Generic template for most substring problems -
https://discuss.leetcode.com/topic/30941/here-is-a-10-line-template-that-can-solve-most-substring-problems/10
int findSubstring(string s){
        vector<int> map(128,0);
        int counter; // check whether the substring is valid
        int begin=0, end=0; //two pointers, one point to tail and one  head
        int d; //the length of substring

        for() { /* initialize the hash map here */ }

        while(end<s.size()){

            if(map[s[end++]]-- ?){  /* modify counter here */ }

            while(/* counter condition */){

                 /* update d here if finding minimum*/

                //increase begin to make it invalid/valid again

                if(map[s[begin++]]++ ?){ /*modify counter here*/ }
            }

            /* update d here if finding maximum*/
        }
        return d;
  }


Intuition behind the solition:
In any sliding window based problem we have two pointers. One right pointer whose job is to expand the current
window and then we have the left pointer whose job is to contract a given window.

At any point in time only one of these pointers move and the other one remains fixed.

We keep expanding the window by moving the right pointer. When the window has all the desired characters, we contract
(if possible) and save the smallest window till now.
"""
import collections


def minWindow(s, t):
    """
    The current window is s[i:j] and the result window is s[I:J].
    In need[c] I store how many times I need character c (can be negative) and missing tells how many characters
    are still missing. In the loop, first add the new character to the window.
    Then, if nothing is missing, remove as much as possible from the window start and then update the result.
    :param s:
    :param t:
    :return:
    """
    # need is initialized to Counter({'A': 1, 'B': 1, 'C': 1}) if t = "ABC"
    need, missing = collections.Counter(t), len(t)

    i = I = J = 0
    for j, c in enumerate(s, 1):  # starts j from 1 instead of 0; j represents the right end of sliding window,
        # the leading end
        missing -= need[c] > 0  # if need[c] > 0 it subtracts 1 ie True is type-casted to 1, False to 0
        need[c] -= 1
        if not missing:  # if missing > 0 => enters condition
            while i < j and need[s[i]] < 0:
                need[s[i]] += 1
                i += 1  # advance the left index of sliding window ie the trailing end, hence shrinking it
            if J == 0 or j - i <= J - I:
                I, J = i, j
    return s[I:J]
