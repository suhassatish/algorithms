"""
Diagnosing memory leaks in Java - Main sources:
1) When a class manages its own memory, for exmaple - resizing array implementation of queue.
When an element is freed, any object references contained in the element should be nulled out.
eg -
public Object pop() {
    if (size == 0)
        throw new EmptyStackException()
    Object result = element[--size]
    element[size] = null; //eliminate obsolete reference
}
Nulling out object references should be the exception rather than the norm.

2) Another source of mem leaks is caches. Easy to forget an object's reference exists in cache
until long after it becomes irrelevant. To prevent this, you may represent caches as a WeakHashMap.
Entry in WeakHashMap is relevant only as long as there are references to keys outside the cache.
Its not useful when there are external references to the values associated with the keys.

3) If you implement an API where clients register callbacks but dont de-register them explicitly,
they will accumulate causing memory leaks. Solution is again, storing them as WeakHashMap.
"""