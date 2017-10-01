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
    need, missing = collections.Counter(t), len(t)
    i = I = J = 0
    for j, c in enumerate(s, 1):
        missing -= need[c] > 0
        need[c] -= 1
        if not missing:
            while i < j and need[s[i]] < 0:
                need[s[i]] += 1
                i += 1
            if not J or j - i <= J - I:
                I, J = i, j
    return s[I:J]