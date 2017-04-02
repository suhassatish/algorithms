"""
Notes from Elasticon 2017 and the ELK stack (elastic_search - logstash - kibana)

-----------
Scaling with Elastic at Blizzard entertainment, maker of games like Diablo 3, World of Warcraft,
starcraft

Blizzard data_lake v1 architecture:
Game Server   ->  RabbitMQ -> Flume -> Hadoop HDFS -> Map-Reduce
                     ^
Game clients -> API -|

Pros of this architecture:
1) Foundation of data-driven workstream
2) Protocol buffers well established
Cons:
1) Writing Map-Reduce needed specialized expertise
2) Scaling RabbitMQ became a challenge, its non-trivial
3) Schemas co-ordinated via email (if at all)

Goals for v2 architecture -
1) ~20 Billion messages/day
2) Schema registry
3) Collect data from anywhere
4) Free the data

v2 architecture -
Git repo for schemas - automatic versioning

Game Server -> Logs    -> Logstash  ->|
    |->        Metrics -> Logstash   -|
                                      V
                                     Kafka -> Hadoop HDFS -> Map-reduce
                                      ^   \
Game client -> SDK -> API ->    ->    |   \-> Elastic Search -> Tribe -> Kibana

Wins -
1) near-real time debugging from client data => new ways to debug
2) searchable logs, good bye grep!
3) N/W quality reports; measurable customer impact even better than server monitoring
4) SDKs for multiple languages/platforms
"""