"""
Code a simple bloom filter.

1) Read words of an English dictionary from a file. A large number (> 100K) is required.
 Create one or use one on your system, eg- /usr/share/dict/words

2) Add the words to a bloom filter (not a hash table but a bloom filter)

3) Look up random words from the bloom filter

4) Do a comparison with linear-time searching the dictionary. You can also compare with hash-table,
but depending on how fast our machine is and how large your data-set is, speed-up may or may not
be seen.

Ref - http://www.maxburstein.com/blog/creating-a-simple-bloom-filter/
Bloom filters tell us whether or not an item exists in a collection, very quickly, just by checking
a few bits. Bloom filters may return some false positives, but never return false negatives.
We can control the amount of false positives we receive by trade-off time and memory.

Practical applications: Google chrome web browser maintains a bloom filter of malicious URLs.
This helps prevent pinging google servers to check if a site is a malicious link.

Cassandra also uses bloom filters to save IO when performing a key lookup. Each(sorted string) table
has a bloom filter associated with it that Cassandra checks before doing any disk seeks, making
queries for keys that dont exist almost free.
"""


# pip install bitarray
# pip install mmh3
from bitarray import bitarray
import mmh3


class BloomFilter(object):

    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, string):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            self.bit_array[result] = 1

    def lookup(self, string):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            if self.bit_array[result] == 0:
                return "Nope"
        return "Probably"


def main():
    """
    Method to test code
    :return:
    """
    bf = BloomFilter(500000, 7)
    huge = set()
    lines = open("/usr/share/dict/web2").read().splitlines()  # default path exists on mac_OS_X
    for line in lines:
        bf.add(line)
        huge.add(line)

    # print bf.lookup("google")  # Probably
    # print bf.lookup("Max")  # Probably
    # print bf.lookup("mice")  # Probably
    # print bf.lookup("3")  # Nope

    import datetime
    start = datetime.datetime.now()
    bf.lookup("google")
    end = datetime.datetime.now()
    print (end-start).microseconds  # 1460

    start = datetime.datetime.now()
    for word in huge:
        if word == "google":
            break
    finish = datetime.datetime.now()
    print (finish-start).microseconds  # 26,563

    start = datetime.datetime.now()
    if 'google' in huge:
        print "exists"
    finish = datetime.datetime.now()
    print (finish-start).microseconds  # 4

    start = datetime.datetime.now()
    bf.lookup("apple")
    finish = datetime.datetime.now()
    print (finish-start).microseconds  # 26

    start = datetime.datetime.now()
    for word in huge:
        if word == "apple":
            break
    finish = datetime.datetime.now()
    print (finish-start).microseconds  # 22,558
    # conclusion: hashset is faster than bloom_filter, but memory footprint is huge.
    # when memory constrained, bloom_filter is a good choice.


if __name__ == '__main__':
    main()
