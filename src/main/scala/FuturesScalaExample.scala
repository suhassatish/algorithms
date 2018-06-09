//Spark job with async HTTP call
//https://stackoverflow.com/questions/35899843/spark-job-with-async-http-call/45946369#45946369

// Break down your huge workload into smaller chunks, in this case huge query string is broken 
// down to a small set of subqueries
// Here if needed to optimize further down, you can provide an optimal partition when parallelizing
val queries = sqlContext.sparkContext.parallelize[String](subQueryList.toSeq)

// Then map each one those to a Spark Task, in this case its a Future that returns a string
val tasks: RDD[Future[String]] = queries.map(query => {
    val task = makeHttpCall(query) // Method returns http call response as a Future[String]
    task.recover { 
        case ex => logger.error("recover: " + ex.printStackTrace()) }
    task onFailure {
        case t => logger.error("execution failed: " + t.getMessage) }
    task
})

// Note:: Http call is still not invoked, you are including this as part of the lineage

// Then in each partition you combine all Futures (means there could be several tasks in each partition) and sequence it
// And Await for the result, in this way you making it to block untill all the future in that sequence is resolved

val contentRdd = tasks.mapPartitions[String] { f: Iterator[Future[String]] =>
   val searchFuture: Future[Iterator[String]] = Future sequence f
   Await.result(searchFuture, threadWaitTime.seconds)
}

// Note: At this point, you can do any transformations on this rdd and it will be appended to the lineage. 
// When you perform any action on that Rdd, then at that point, 
// those mapPartition process will be evaluated to find the tasks and the subqueries to perform a full parallel http requests and 
// collect those data in a single rdd. 

