"""
Netflix Blog -
https://medium.com/netflix-techblog/reactive-programming-in-the-netflix-api-with-rxjava-7811c3a1496a

Server-side concurrency is needed to effectively reduce network chattiness.
Each network request from a client device watching Netflix is inherently parallel with other client
requests.

If the server-side execution of a single collapsed "heavy" request does not achieve a
similar level of parallel execution it may be slower than the multiple "light" requests, even
accounting for saved network latency.

1) Java futures are expensive to compose. Although java futures are straight-forward for a single
level of asynchronous execution, they start to add non-trivial complexity when they're nested (prior
to java8 CompletableFuture).

It also blocks prematurely on Future.get(), eliminating the benefit of async exe. Latency of each
request varies unpredictably at runtime. So conditional async exe becomes error-prone to compose.

2) Callbacks have their own problem: They offer solution to the blocking problem on calling
Future.get() by not allowing anything to block. They are naturally efficient because they execute
when the response is ready. But they too become unwieldy with nested composition.
----------------------------------------------------------------------------------------
Reactive programing offers efficient exe and composition by providing a collection of operators
capable of filtering, selecting, transforming, combining and composing observables.

TODO - make notes from above link.

Related articles - https://www.slideshare.net/kasun04/reactive-programming-in-java-8-with-rxjava
TODO

----------------------------------------------------------------------------------------
TODO - make notes from below related blog
https://medium.com/netflix-techblog/optimizing-the-netflix-api-5c9ac715cf19
"""