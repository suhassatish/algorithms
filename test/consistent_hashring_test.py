#source: http://techspot.zzzeek.org/2012/07/07/the-absolutely-simplest-consistent-hashing-example/
import unittest
import collections
import random
import math
from app.consistent_hashring import ConsistentHashRing

class ConsistentHashRingTest(unittest.TestCase):
    def test_get_distribution(self):
        ring = ConsistentHashRing(100)

        numnodes = 10
        numhits = 1000
        numvalues = 10000

        for i in range(1, 1 + numnodes):
            ring["node%d" % i] = "node_value%d" % i

        distributions = collections.defaultdict(int)
        for i in xrange(numhits):
            key = str(random.randint(1, numvalues))
            node = ring[key]
            distributions[node] += 1

        # count of hits matches what is observed
        self.assertEquals(sum(distributions.values()), numhits)

        # I've observed standard deviation for 10 nodes + 100
        # replicas to be between 10 and 15.   Play around with
        # the number of nodes / replicas to see how different
        # tunings work out.
        standard_dev = self._pop_std_dev(distributions.values())
        self.assertLessEqual(standard_dev, 20)

        # if the stddev is good, it's safe to assume
        # all nodes were used
        self.assertEquals(len(distributions), numnodes)

        # just to test getting keys, see that we got the values
        # back and not keys or indexes or whatever.
        self.assertEquals(
                set(distributions.keys()),
                set("node_value%d" % i for i in range(1, 1 + numnodes))
            )

    def _pop_std_dev(self, population):
        mean = sum(population) / len(population)
        return math.sqrt(
                sum(pow(n - mean, 2) for n in population)
                / len(population)
            )