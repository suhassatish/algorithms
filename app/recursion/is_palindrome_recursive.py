"""
check if a string is a palindrome using recursion

Ignore punctuation, case and whitespace
"""
import string


def is_palindrome(s):
    s = s.replace(" ", "").translate(None, string.punctuation).lower()
    # http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
    # 1) translate is fastest as it uses C lookups from a map

    # 2) regex is 2nd fastest;
    # regex = re.compile(['%s'] % re.escape(string.punctuation)); regex.sub('', s)

    # 3) s.replace(c, "") is the slowest, almost 4 times slower, and works character by character
    return _is_palindrome(s)


def _is_palindrome(s):
    # print s
    # import ipdb; ipdb.set_trace()
    if s is None or len(s) in (0, 1):
        return True

    elif s[0] != s[-1]:
        return False

    else:
        return _is_palindrome(s[1:len(s)-1])


# print is_palindrome('racecar')
print(is_palindrome('Never a foot too far, even.!'))