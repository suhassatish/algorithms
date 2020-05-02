"""
ScheduleID is something that is required to set the SLA on an AZK project. ScheduleID is something thats included in the
URL when you set the SLA.

If a DAG is too long, azkaban has issues.

There is no way you can run an 800MB java process on SIQ Azkaban
If you want to do that, you will need to submit the job as a YARN application to run on EMR.
Azkaban simply doesnt provide resource management, so we cant have large processes running on it.

But with YARN, there can be other issues, like it killing the executor container because it is using too much off-heap
memory. Can try to boost boost `spark.yarn.executor.memoryOverhead`. 6 GB was low for this setting for an SIQ app, try
16 GB.
    numExecutors : 80
    executorMem: 8g
    numberCore: 1
    executorOverhead: 4g

"""