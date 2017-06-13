"""
Write a function that, given a string (such as 'AABBCCCCCBABAA') returns
the character with the longest consecutive substring. In this case, it is C,
because there are 5 Cs in a row, which trump all other characters.

Asked in Twilio phone screen
"""


def longest_consecutive_substring_char(s):
    if s is None:
        return None
    if len(s) == 0:
        return s
    if len(s) == 1:
        return (s, 1)
    
    longest_char = None
    longest_count = 0
    i = 0
    ip1 = 1
    while i <= len(s) - 3:  # goes upto len(s) - 2
        # ip1 = i + 1
        count = 1

        while i <= len(s) - 2 and (s[i] == s[ip1]):
            count += 1
            i += 1
            ip1 += 1
            if count > longest_count:
                longest_count = count  # 2
                longest_char = s[i]  # A
        else:
            count = 1
            i += 1 # i = 2
            ip1 += 1 # ip1 = 3

    return longest_char,longest_count
               
if __name__ == '__main__':
    print longest_consecutive_substring_char('AABBCCCCCBABAA')
    print longest_consecutive_substring_char(None)
    print longest_consecutive_substring_char('')
    print longest_consecutive_substring_char('AAAAAA')
    print longest_consecutive_substring_char('abfffaaaafff')
    print longest_consecutive_substring_char('a')
