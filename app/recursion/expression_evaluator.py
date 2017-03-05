"""
Given a string of integers as input, put between each pair of digits, one of {'', '*', '+'}
such that the expression you get will evaluate to K (a number also given as input).

Putting an empty string means, the numbers are joined to form a new number (eg  1 "" 2 = 12)

Order of integers in the input needs to remain the same.

eg - input = string = "222", K = 24
possible output solutions = "22+2", or "2+22"

Precedence of operators: "" > "*" > "+"
"""
from collections import deque


def is_valid_expr(s, target):
    # time complexity according to EPI 25.27 - synthesize an expression = O(n * 3^n)
    input_list = [int(i) for i in list(s)]
    operators = []
    operands = []
    return _is_valid_expr(input_list, target, 0, 0, operands, operators)


def _is_valid_expr(input_digit_list, target, curr_term, offset, operands, operators):
    curr_term = curr_term * 10 + input_digit_list[offset]

    if offset == len(input_digit_list) - 1:
        operands.append(curr_term)

        if evaluate(operators, operands) == target:  # found a match
            res = []
            operand_index = 0
            res.append(operands[operand_index])

            for optr in operators:
                operand_index += 1
                res.append(optr)
                res.append(operands[operand_index])

            res.append('=')
            res.append(target)
            return ''.join([str(x) for x in res])

        operands.pop()
        return False

    # no operator
    if _is_valid_expr(input_digit_list, target, curr_term, offset + 1, operands, operators):
        return True

    # tries multiplication operator *
    operands.append(curr_term)
    operators.append('*')
    if _is_valid_expr(input_digit_list, target, curr_term, offset + 1, operands, operators):
        return True
    # back-track
    operands.pop()
    operators.pop()

    # tries addition operator +
    operands.append(curr_term)
    operators.append('+')

    # slight optimization for addition to backtrack earlier
    # if target - evaluate(operands, operators) <= remaining_int(input_digit_list[offset+1:]):
    if _is_valid_expr(input_digit_list, target, curr_term, offset + 1, operands, operators):
        return True

    # back-track
    operands.pop()
    operators.pop()

    # exhausted trying all possibilities
    return False


def remaining_int(input_digit_list):
    val = 0
    for d in input_digit_list:
        val = val * 10 + d
    return val


def evaluate(operators, operands):
    intermediate_operands = deque()
    operand_index = 0
    intermediate_operands.appendleft(operands[operand_index])
    operand_index += 1

    # evaluates '*" first
    for oper in operators:
        if oper == '*':
            intermediate_operands.appendleft(
                intermediate_operands.popleft() * operands[operand_index])
            operand_index += 1
        else:
            # not sure what this is. Maybe "" operator. Reproduced and ported from java from source:
# http://elementsofprogramminginterviews.com/static/solutions/java/src/main/java/com/epi/AddOperatorsInString.java
            intermediate_operands.appendleft(operands[operand_index])
            operand_index += 1

    # evaluates '+' second
    # not sure why this is outside the 'for' loop above
    summ = 0
    while intermediate_operands:
        summ += intermediate_operands.popleft()
    return summ
