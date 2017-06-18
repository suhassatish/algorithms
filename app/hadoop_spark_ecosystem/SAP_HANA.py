"""
SAP HANA is an in-memory OLAP DB with integrations to the hadoop ecosystem.

SAP Tooling eco-system:
1)
Smart Data Access: in case you need to read data out of Hadoop, you can use SAP HANA Smart Data
Access (SDA) to do it. SDA is widely used when it comes to hybrid models (SAP HANA + SAP NetWeaver
BW powered by SAP HANA) or even Near Line Storage (NLS) scenarios. You can basically access a
'table' in a different repository (mainstream databases all included) from SAP HANA without
actually having to bring the data over to SAP HANA. So you could have your 'hot' data in SAP HANA
and your cold data into Hadoop and using SDA a simple UNION would bring data from both 'tables'
together.

2)
SAP BusinessObjects Universe: in case you only need to report in Hadoop data out of SAP
BusinessObjects Suite, you can combine data from any source to Hadoop using the Universe,
SAP BusinessObjects semantic layer to get the job done. There you can setup relationships, rules,
etc.

3)
SAP DataServices 4.1 (and above): in case you really need to bring data from Hadoop into SAP HANA
and maybe apply some heavy transformation on the way, that is your path to go. SAP DataServices have
been tunned to been able to read and write huge amount of data both ways.

4)
SAP Lumira: in case you only need front-end integration and less complex data handling and
transformation, that is a easy way to go. SAP Lumira can access and combine data from Hadoop (HDFS
Data Set, Hive or Impala Data Set or a SAP Vora Data Set) and SAP HANA.

5)
SAP Vora: in case you need to correlate Hadoop and SAP HANA data for instant insight that drives
contextually-aware decisions that can be processes either on Hadoop or in SAP HANA

Adobe uses Hadoop with SAP Data Services because of the volume of data. The Hadoop component is
tracking all of the events that happen in the Adobe Creative Cloud.

Cost:
HANA costs a lot of money.  A typical deployment would be $1M+ in just hardware, not to mention at
least as much in software.  Yes you can do HANA in the cloud, and you can buy hardware for as cheap
as ~$100k that is supported, but this would be a sandbox environment. Nothing from SAP is
inexpensive.  You would use this for extremely fast analytical reporting, it is the Ferrari of
databases.

Also read: https://db-engines.com/en/system/HBase%3BHive%3BSAP+HANA
Hbase vs Hive vs SAP Hana comparison chart
"""