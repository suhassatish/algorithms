"""
mirrored from git://git.apache.org/spark.git
Branch: master spark/examples/src/main/python/pagerank.py

This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx
Example Usage:
bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10

Pinterest onsite interview question.
PageRank Algorithm -
1) Initialize each page's rank to 1.0

2) On each iteration, have each page p send to its neighboring pages, the computed value of
    rank(p)/numNeighbors(p)

3) Set each page's rank = 0.15 + 0.85 * contributionsReceived

Steps 2) and 3) repeat for several iterations, during which the algorithm will converge to the
correct pageRank value for each page. In practice, its typical to run about 10 iterations.

http://www.openkb.info/2016/03/understanding-pagerank-algorithm-in.html
Explains the key-value transformations as the pageRank algorithm transforms data in a spark pipeline
Assume you have 4 pages with links in an adjacency list represented as below (outgoing links)-
Google: [MapR]
Blogger: [Google, Baidu]
Baidu: [MapR]
MapR: [Baidu, Blogger]

Lets walk through the pageRank algorithm described above, as implemented in Spark
1) val links = sc.parallelize(List(
        ("MapR",List("Baidu","Blogger")),
        ("Baidu", List("MapR")),
        ("Blogger",List("Google","Baidu")),
        ("Google", List("MapR"))
        )).partitionBy(new HashPartitioner(4))
        .persist()

val ranks = links.mapValues(v => 1.0)

2) On each iteration, have each page p send to its neighboring pages, the computed value of
    rank(p)/numNeighbors(p)

val contributions = links.join(ranks).flatMap {
    case (url, (links, rank)) => links.map( dest => (dest, rank / links.size))
   }
# contributions.collect will contain the incoming pageRank weights for each page like below -
Array[(String, Double)] = Array((MapR,1.0), (Baidu,0.5), (Blogger,0.5),
                                (Google,0.5), (Baidu,0.5), (MapR,1.0))

3) Set each page's rank = 0.15 + 0.85 * contributionsReceived
val ranks = contributions.reduceByKey((x, y) => x + y).mapValues(v => 0.15 + 0.85 * v)

----------------
PageRank computation needs repeated joining of 2 RDDs - namely Neighbors(id, edges)
Ranks(id, rank) which looks like rank_vector = [(id1, rank1), (id2, rank2), (id3, rank3)].
Explained in https://stanford.edu/~rezab/slides/maryland_intro.pdf
Requires repeatedly hashing together page adjacency list and rank vector.

"""
from __future__ import print_function

import re
import sys
from operator import add

from pyspark.sql import SparkSession


def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)


def parseNeighbors(urls):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[1]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pagerank <file> <iterations>", file=sys.stderr)
        exit(-1)

    print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
          "Please refer to PageRank implementation provided by graphx",
          file=sys.stderr)

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("PythonPageRank")\
        .getOrCreate()

    # Loads in input file. It should be in format of:
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     ...
    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    # input file is an adjacency list of pairs like [(1, 2), (1, 3), (1, 4), (2, 1), (3, 1), (4, 1)]
    # SparkSession.read returns a DataFrameReader that can be used to read data in as a DataFrame

    # Loads all URLs from input file and initialize their neighbors.
    links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()

    # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[2])):
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(
            lambda url_urls_rank: computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)
        # reduceByKey() does something like a map-side combine, before shuffling. Hence reduces N/W
        # shuffle data compared to groupByKey which creates a ShuffledRDD

    # Collects all URL ranks and dump them to console.
    for (link, rank) in ranks.collect():
        print("%s has rank: %s." % (link, rank))

    spark.stop()
