"""
Notes from Facebook's type ahead search architecture blog -
https://www.facebook.com/notes/facebook-engineering/the-life-of-a-typeahead-query/389105248919/

1) As the user clicks on search box in facebook, a query is sent to get the user's friends, events,
pages and bring them into the browser cache.

2) If objects are already in the browser cache, an AJAX request is sent not to fetch those again.
This request contains the search query string along with objects that are already in browser cache.
The load balancer routes the request to an appropriate web machine.

3) Aggregator service - This is a stateless php AJAX endpoint, a thin wrapper around a thrift
service for handling typeahead queries. This service is at the root of a tree of separate search
services. It has no index of its own. It delegates queries to multiple lower-level services in
parallel and integrates the results.

4) Leaf services - Each search services scours its indexes for results that prefix-match the
contents of search-box.
    a) Each leaf service is designed to retrieve and rank results on only a few specific features.

    b) Global service: Maintains an index of all pages and applns on the site. No personalization.
    eg features- i) Rank applns by #users interacted with it in last month
                ii) Rank pages by the structure of the graph around them
        Results from this service are independent of user, hence can be query-cached in memcached.

    c) Graph service: Searches user's neighborhood of graph and returns results. User and friend's
    graph connections can be a powerful signal of expressed preferences and thus, relevance.
    Graph contain 400M active users, and billions of connections, both among users, to objects of
    other types: pages, applications, events, etc

5) Merging results - Aggregator merges results and features returned from each leaf service and
 ranks results according to model. Top results are returned to the web tier.

6) Fetching data and validating results - Results are just list of ids. Web tier needs to lookup
these ids from mysql/memcached, fetch, denormalize and render data such as name, profile picture,
link, shared networks, mutual friends, etc. Web tier also needs to do privacy filtering, if user is
allowed to see each result.

7) Displaying the results: Results from 6) above are sent sent to browser & also cached in browser
along with bootstrapped connections so that similar subsequent queries dont hit the backend again.
----------------------------------------
Testing in the dark pre-launch -
1) Tested by returning results for every key-stroke. Unearthed network bottlenecks. Hence, adjusted
topology of architecture.

2) Several variants of UI/UX A/B tested. Some trade-offs here:
    a) number of results - Just enough to make surprising useful discoveries, without getting
        overwhelmed. But showing fewer results = faster & less distracting. Final design - Adjusts
        number of results based on browser window height.

    b) Mouse vs keyboard - Non-technical user prefers mouse

    c) Searching - Although enter-key auto-selects first result, but still ensure users who wanted
    to search were taken to "See More Results" page.

    Other considerations - highlighting query search string in results, distinguishing b/w different
    types of results - ppl vs pages vs applns.

    Many search trilemmas are between performance vs recall vs relevance. At FB, focus was on perf,
    as spending > 100 ms to retrieve a result will cause typeahead to "stutter".
"""