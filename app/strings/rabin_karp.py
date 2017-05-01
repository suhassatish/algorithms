"""
Substring search using hashing, in linear time
http://algs4.cs.princeton.edu/lectures/53SubstringSearch.pdf

During hashing, its important to keep numbers small to prevent overflow. You can use the following
Math trick for that-
2 useful modular arithmetic identities -
(a + b) mod Q = ((a mod Q) + (b mod Q)) mod Q
(a * b) mod Q = ((a mod Q) * (b mod Q)) mod Q
"""


class RabinKarp(object):
    def __init__(self, pat):
        self._M = len(pat)  # pattern length
        self._R = 256  # radix
        self._Q = 997  # a long random prime is better for security reasons, but avoid overflow

        self._RM1 = 1  # pre-compute R**(M-1) (mod Q)
        for i in xrange(1, self._M):
            self._RM1 = (self._R * self._RM1) % self._Q

        self._pat_hash = self._hash(pat)  # pattern hash value

    def _hash(self, txt):
        """
        Compute hash for M-digit pattern.
        If t[i] = i'th character in a text,
        x[i] = t[i] * R** M-1 + t[i+1] * R** M-2 + ...t[i+M-1] * R**0 (mod Q)

        Uses horner's method (illustrated below) to evaluate degree-M polynomial in linear-time
        pat[i]
        i 0 1 2 3 4
          2 6 5 3 5
        If Q (modulo) = 997 , R (radix) = 10
        0 => 2 % 997 = 2
        1 => 2 * 10 + 6 % 997 = 26
        2 => 26 * 10 + 5 % 997 = 265
        3 => 265 * 10 + 3 % 997 = 659
        4 => 659 * 10 + 5 % 997 = 613
        :return: long integer
        """
        h = 0
        for j in xrange(self._M):
            h = (h * self._R + ord(txt[j])) % self._Q
        return h

    def search(self, txt):
        """
        Monte-carlo version - Return match if hash match. Disadv - hash collisions will cause F+
        Pro: Always runs in linear time, extremely likely to return correct answer (but not always!)

        Las-Vegas version handles hash collision by checking for substring match if hash match, and
        continues search if false collision. Always returns correct answer. Extremely likely to run
        in linear time, but worst case is MN

        Checks for hash collision using rolling hash function.
        x[i] = t[i] * R** M-1 + t[i+1] * R** M-2 + ...t[i+M-1] * R**0 (mod Q)

        x[i+1] = (x[i] - t[i] * R** M-1) * R + t[i+M]
        where x[i] = current value; t[i+M] = add new trailing digit
        The above formula can be simplified as
        (curr_value - subtract_leading_digit) * multiply_by_radix + add_new_trailing_digit
        eg - (41932 - 40000)*10 + 6 = 19326



        :param txt: text to search for pattern match
        :return:
        """
        n = len(txt)
        txt_hash = self._hash(txt)
        if self._pat_hash == txt_hash:
            return 0

        # now compute the rolling hash on the text by sliding the pattern over the text, and reusing
        # previously computed txt_hash
        for i in xrange(self._M, n):
            txt_hash = (txt_hash + self._Q - self._R * self._M * ord(txt[i - self._M]) % self._Q) %\
                       self._Q
            txt_hash = (txt_hash * self._R + ord(txt[i])) % self._Q
            if self._pat_hash == txt_hash:
                return i + 1 - self._M  # found, return index of start of first match
        return n  # not found

if __name__ == '__main__':
    for pat, txt in [('abracadabra', 'abacadabrabracabracadabrabrabracad'),  # 14
                     ('rab', 'abacadabrabracabracadabrabrabracad'),  # 8
                     ('bcara', 'abacadabrabracabracadabrabrabracad'),  # 34 (not found)
                     ('rabrabracad', 'abacadabrabracabracadabrabrabracad'),  # 23
                     ('abacad', 'abacadabrabracabracadabrabrabracad')]:  # 0
        rk = RabinKarp(pat)
        print rk.search(txt)  # TODO - doesnt work, debug test cases
