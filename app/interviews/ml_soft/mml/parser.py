"""MML Syntax Checker

Provide an implementation for parse(mml) -> Result as per the exercise details
  mml -- The contents of the mml file to check
  returns a result as a string with the form:
    {{valid: boolean, error: {line: number, type: string}}}

You can use the helpers functions valid and invalid to return the result as
the expected string representation.
There is also global variables defined with the error types defined in the spec.
"""

import json
import re
from collections import OrderedDict

# Character not allowed in tag name
WRONG_CHAR_IN_TAG_NAME = 'WRONG_CHAR_IN_TAG_NAME'
# Too many/few characters in tag name.
WRONG_NUMBER_CHARS_IN_TAG = 'WRONG_NUMBER_CHARS_IN_TAG'
# Closed tag (aka: >) without an opening pair
UNEXPECTED_CLOSING_TAG_CHAR = 'UNEXPECTED_CLOSING_TAG_CHAR'
# No closed tag for an open tag or closing tag with an open pair
UNBALANCED_TAG = 'UNBALANCED_TAG'
# Tag is opened with '<' character, but no matching '>' character was seen
UNCLOSED_TAG = 'UNCLOSED_TAG'
# CDATA section not closed before end of file
UNEXPECTED_END_OF_STREAM = 'UNEXPECTED_END_OF_STREAM'


def valid():
    """Return a representation of a valid result"""
    return json.dumps({'valid': True})


def invalid(line='', error_type=''):
    """Return a representation of an invalid result"""
    error = OrderedDict([('line', line), ('type', error_type)])
    return json.dumps(OrderedDict([('valid', False), ('error', error)]))


def parse(mml):
    # Add implementation here
    # examples:
    #   return valid()
    #   return invalid(line=4, error_type=WRONG_CHAR_IN_TAG_NAME)
    mmlv = MmlValidator(mml)
    boolean_result, line, error_type = mmlv.validate()
    if boolean_result:
        return valid()

    else:
        return invalid(line, error_type)


class MmlValidator(object):
    def __init__(self, mml):
        self.mml = mml
        self.BUFFER_SIZE = 80

    def validate(self):
        return self.valid_open_close_chars()

    def valid_open_close_chars(self):
        tags_stk = []
        line_number = 1
        while not self.mml.is_eof():
            c = self.mml.next_char()
            if not self.mml.is_eof():
                next_c = self.mml.next_char()
            else:
                next_c = ''

            if c == '<':

                if next_c == '/':
                    tags_stk.append('</')
                else:  # check if next_c is invalid char
                    tags_stk.append('<')

                count = 0
                while count <= 11 and not self.mml.is_eof() and next_c != '>':
                    next_c = self.mml.next_char()
                    if not self.mml.is_eof and not 65 <= ord(next_c) <= 90:
                        return False, line_number, WRONG_CHAR_IN_TAG_NAME
                    count += 1

                if count > 11 or count < 2:
                    return False, line_number, WRONG_NUMBER_CHARS_IN_TAG
                if self.mml.is_eof():
                    return False, line_number, UNEXPECTED_END_OF_STREAM
                if next_c == '>':
                    tags_stk.pop()  # we found a matching closing bracket
                if not self.mml.is_eof() and not 65 <= ord(next_c) <= 90:
                    return False, line_number, WRONG_CHAR_IN_TAG_NAME

            elif c == '>':
                if len(tags_stk) != 0:
                    return False, line_number, UNEXPECTED_CLOSING_TAG_CHAR

            # now increment line_number
            elif c == '\n':
                line_number += 1

        # if we reached the end of the while loop and didn't return yet, then its valid
        return True, None, None


# Hello<>World !</>

# <BODY>Hello<B>World !</B>
# <REALLY_>To The Planet</REALLY_x>


### Phase 1 - detect invalid tags
# - A tag must be opened by `<` or `</` and must be then closed by a `>` character (`<HELLO`, `</HI` are invalid)
# - A tag name must have at least one, and no more than 10 characters (`<HELLOOOOOOOOOO>` is invalid)
# - A tag name must be upper-case and alphabetic. (`<HELLO-1.0>`, `<hellow>` are invalid)
# - Content must not include dangling `>` characters. (`this is some content>` is invalid)
