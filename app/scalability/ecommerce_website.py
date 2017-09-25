"""
2 important things to clarify in interview -
Are they expecting an object-modeling type of interview? OR An architectural scaling system design on how to maintain
high availability?

For an object modeling, focus on entities like Products, Buyers, Sellers, shopping cart, etc
For a scalability system design, its similar to caches and CAP theorem trade-offs.
------------------------------------------------------------------------------------------------------------------------

Design product view history feature for full-featured high-traffic eCommerce website like Amazon.com
Use case: user browses a number of items. Back on home page, he's shown all N recently viewed items.
Define API/object model.
Backend service has to store all data in-memory: no DB available.
If N = number of recently viewed items, data structure has to process update in O(1) and retrieve history in O(N)


"""