"""
Cost-based optimizer in Hive -
https://cwiki.apache.org/confluence/display/Hive/Cost-based+optimization+in+Hive

https://hortonworks.com/blog/hive-0-14-cost-based-optimizer-cbo-technical-overview/
With diagrams

4 STEPS IN ANY COST-BASED OPTIMIZER (CBO IN HIVE IS CALLED CALCITE) -
1) Query parsing and validation

2) Generate possible execution plans (agnostic of execution engine)

3) For each logically equivalent plan, assign a cost (based on selectivity and cardinality of
logical operators)

4) Select the plan with the lowest estimated cost
-------------------------
Join ordering is the most difficult and important optimization for performance.
Estimating data-skew & column cardinality are important pre-requisite statistics
  a) table size
  b) column statistics for each column- min, max, avg, count(distinct values)
  c) In the absence of value-range-histograms, column distributions are assumed to follow uniform
  distributions

Query optimizer considers 2 different types of join trees -
1) Left-deep trees- Each internal node has atleast 1 leaf as a child. This doesn't result in efficient
join plans for snowflake schemas.

2) Bushy trees- Here the tree heights on the left and right are more balanced.
eg - join(A,B) join join(C,D)
Refer chart on Hortonworks blog.
Bushy tree is constructed using the property of Predicate pushdown to use the most selective filters
in the earliest joins to reduce downstream data size for other subsequent joins.
----------------------------------
Another cost model (Calcite Volcano) considers I/O RD/WR cost to local disk & HDFS, N/W shuffle cost
and CPU cost.
HDFS read is assumed to be 1.5 times of local disk read and
HDFS write is assumed to be 10 times of local disk write.

Following are the assumed values for cost variables:
CPUc = 1 nano sec  = CPU cost for a comparison
NEt = 150 * CPUc nano secs = Avg cost of Tx 1 byte over hadoop cluster from any node to any node
Lw = 4 * NEt = write to local disk
Lr = 4 * NEt = read from local disk
Hw = 10 * Lw = HDFS write
Hr = 1.5 * Lr = HDFS read

For table scan operator, IO usage =  Hr * T(R) * Tsz
where T(R) = number of tuples in relation R; Tsz = size of Tuple (compressed and serialized on disk)

"""
