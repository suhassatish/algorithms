"""
Consider four numbers: , , , and . You must change at most  bits in  and  to form the numbers  and  satisfying the equation . Here, the | symbol denotes the bitwise OR operation.

Given  sets of the numbers defined above, find and print the respective values of  and  on new lines; if no such value exists, print  instead. If there are multiple solutions, make  as small as possible; if there are still multiple solutions, make  as small as possible.

Note:

, , and  are given in Hexadecimal (base 16), and  is given in decimal (base 10).

If number of bits changed in  is  and number of bits changed in B is , than  must be smaller or equal to .

Input Format

The first line contains an integer, , denoting the number of queries. The subsequent lines describe each respective query as follows:

The first line contains a single integer denoting the value of .
Each of the next  lines contains a Hexadecimal (base 16) number describing the respective values of , , and .
Constraints

Output Format

Print two lines of output for each query:

The first line should contain a Hexadecimal (base 16) number denoting the value of .
The second line must contain a Hexadecimal (base 16) number denoting the value of .
If no valid answer exists, you must instead print one line of output with the integer .

Note: The letters in Hexadecimal numbers must be in uppercase.

Sample Input

3
8
2B
9F
58
5
B9
40
5A
2
91
BE
A8
Sample Output

8
58
18
42
-1


"""


def equal_left_zero_string_pad(a, b, c):
    num_chars_to_pad = max(map(len, [a, b, c]))
    return (a.rjust(num_chars_to_pad, '0'),
            b.rjust(num_chars_to_pad, '0'),
            c.rjust(num_chars_to_pad, '0'))


def get_4digit_binary(char_str):
    return format(int(char_str, 16), '04b')


def bin2hex(bin_str):
    """doesnt left pad with zeros"""
    return '{:0x}'.format(int(bin_str,2)).upper()


def hex2bin(hex_str):
    """left pads with zeros"""
    return '{:0{width}b}'.format(int(hex_str, 16), width=4*len(hex_str))


def find_msb_index_after_pos(bin_str, pos):
    for i in range(pos, len(bin_str)):
        if bin_str[i] == '1':
            return i
    return -1


def flip_bit(bin_str, index):

    if index < 0 or index >= len(bin_str):
        return ''
    else:
        return str(int(bin_str[index]) ^ 1)


def minimize(a_bin_str, b_bin_str, c_bin_str, remaining_distance):
    """
    :param a_bin_str:
    :param b_bin_str:
    :param c_bin_str:
    :param remaining_distance:
    :return: binary representation of string
    """
    print("minimize() inputs: a_bin_str = %s; b_bin_str = %s; c_hex_str = %s; d = %d" %
          (a_bin_str, b_bin_str, c_bin_str, remaining_distance))
    if remaining_distance == 0:
        return a_bin_str, b_bin_str

    a_minimized = ''
    b_minimized = ''
    for i in range(0,len(c_bin_str)):
        #import ipdb; ipdb.set_trace()
        if c_bin_str[i]=='0':
            a_minimized += a_bin_str[i]
            b_minimized += b_bin_str[i]
            continue

        if c_bin_str[i]=='1':
            if a_bin_str[i] == '1' and b_bin_str[i] == '1':
                a_minimized += flip_bit(a_bin_str, i)
                remaining_distance -= 1
                if remaining_distance == 0:
                    a_minimized += a_bin_str[i+1:]
                    b_minimized += b_bin_str[i:]
                    break
            elif a_bin_str[i]=='1' and b_bin_str[i]=='0':
                if remaining_distance >= 2:
                    a_minimized += flip_bit(a_bin_str, i)
                    b_minimized += flip_bit(b_bin_str, i)
                    remaining_distance -= 2
                    if remaining_distance == 0:
                        a_minimized += a_bin_str[i+1:]
                        b_minimized += b_bin_str[i+1:]
                        break
            else: #a_bin_str[i]=='0' and b_bin_str[i]=='1'
                a_minimized += a_bin_str[i]
                b_minimized += b_bin_str[i]
                continue

    print("minimize() returning a = %s, b = %s" % (a_minimized,b_minimized))
    return a_minimized, b_minimized


            #make sure only b contributes the 1 to c
            #if a is contributing to the 1 instead, flip a and b bits at that index


    #if b == c, keep removing leading 1 from a until a becomes 0 or we run out of remaining_distance
    #whichever occurs first
    d = 0



def find_min_bit_rotation(a, b, c, k):
    #input can be a huge string upto 55k hex digits which is out of range of even double.
    # so have to have a string parsing solution
    a, b, c = equal_left_zero_string_pad(a,b,c)
    a_prime_bin = ''
    b_prime_bin = ''
    distance = 0
    for i in range(0,len(a)):
        a_4digit_binary = get_4digit_binary(a[i])
        b_4digit_binary = get_4digit_binary(b[i])
        c_4digit_binary = get_4digit_binary(c[i])
        a_prime = ''
        b_prime = ''
        for j in range(0,4):
            #a|b already equals c, no shift required
            if int(a_4digit_binary[j]) | int(b_4digit_binary[j]) == int(c_4digit_binary[j]):
                a_prime += a_4digit_binary[j]
                b_prime += b_4digit_binary[j]
                continue

            #a | b != c => there are 2 cases here ie c = 0 or c = 1
            elif c_4digit_binary[j] == '0':
                #make both a and b = 0 if they're not already 0 and increase distance count
                a_bit = a_4digit_binary[j]
                b_bit = b_4digit_binary[j]
                if(a_4digit_binary[j]!='0'):
                    a_bit = '0'
                    distance += 1
                    if distance > k:
                        return -1,-1
                if(b_4digit_binary[j]!='0'):
                    b_bit = '0'
                    distance += 1
                    if distance > k:
                        return -1,-1
                a_prime += a_bit
                b_prime += b_bit

            elif c_4digit_binary[j] == '1':
                #this is the case where a = b = 0 (since if either a or b was already 1, then  a | b would have been = c
                #prefer to increase b over a, as per requirement to keep a as small as possible
                b_bit = '1'
                distance += 1
                if distance > k:
                    return -1, -1
                a_prime += a_4digit_binary[j]
                b_prime += b_bit

        #now convert binary 4-digit string into 1-digit hex string
        a_prime_bin += a_prime
        b_prime_bin += b_prime

    #if there is remaining flips left <=K, use them to minimize A, then minimize B
    a_prime_min, b_prime_min = minimize(a_prime_bin, b_prime_bin, hex2bin(c), k - distance)
    return bin2hex(a_prime_min).lstrip('0'), bin2hex(b_prime_min).lstrip('0')

#if __name__ == "__main__":
n = int(input().strip())
for i in range(0,n):
    K = int(input().strip())
    A = input().strip()
    B = input().strip()
    C = input().strip()
    res_a, res_b = find_min_bit_rotation(A, B, C, K)
    if res_a == -1:
        print(res_a)
    else:
        print(res_a)
        print(res_b)