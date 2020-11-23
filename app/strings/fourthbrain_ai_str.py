"""
Have the function StringChallenge(str) read str which will contain two strings separated by a space.
The first string will consist of the following sets of characters: +, *, $, and {N} which is optional.
The plus (+) character represents a single alphabetic character, the ($) character represents a number between 1-9,
and the asterisk (*) represents a sequence of the same character of length 3 unless it is followed by {N} which
represents how many characters should appear in the sequence where N will be at least 1. Your goal is to determine
if the second string exactly matches the pattern of the first string in the input.

For example: if str is "++*{5} jtggggg" then the second string in this case does match the pattern, so your program
should return the string true. If the second string does not match the pattern your program should return the string
false.

Examples
Input: "+++++* abcdehhhhhh"
Output: false
Input: "$**+*{2} 9mmmrrrkbb"
Output: true
"""


def StringChallenge(strParam):
    str1, str2 = strParam.split(" ")
    str2_cursor = 0
    for index, c in enumerate(str1):
        if c == "+":
            str2_cursor += 1
            if not str2[index].isalpha():
                print("expected alpha char but found {} at {} index {}".format(str2[index], str2, index))
                return False
        elif c == "$":
            str2_cursor += 1
            if not str2[index].isnumeric():
                print("expected numeric char but found {} at {} index {}".format(str2[index], str2, index))
                return False
        elif c == "*":
            # check if this is the end of str1
            repeat_count = 3
            # check the next char if its a "{"
            if index < len(str1) - 1 and str1[index + 1] == "{":
                repeat_count = int(str1[index + 2])
                print("repeat count = {}".format(repeat_count))
            expected_str2_seq = dedupe(str2[str2_cursor : str2_cursor + repeat_count])
            str2_cursor += repeat_count
            if not len(expected_str2_seq) == 1:
                print("expected length of {} is not 1".format(expected_str2_seq))
                return False
        else:
            continue
    if not str2_cursor == len(str2):
        print("{} has more characters left over at index {}".format(str2, str2_cursor))
        return False

    return True


def dedupe(str1):
    st = set()
    for char in str1:
        st.add(char)
    return ''.join(str(element) for element in st)


# keep this function call here
# print(StringChallenge(input()))


if __name__ == '__main__':
    print(StringChallenge("+++++* abcdehhhhhh")) # False
    print(StringChallenge("$**+*{2} 9mmmrrrkbb")) # True
    print(StringChallenge("++*{5} jtggggg")) # True