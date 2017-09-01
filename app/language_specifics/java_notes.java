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

------------------------
Explicit Imports vs import java.io.* wildcard imports -
The real reasons that people use explicit imports rather than wildcard imports are:

1) Explicit imports clearly document what external classes a class is directly using, provided that you don't leave
redundant imports in your code.

2) Explicit imports avoid problems with name collisions arising when you import two packages that contain classes with
the same (simple) class name.

3) Explicit imports avoid fragility problems where someone adds a new class to some package that you have wildcard
imported. This can lead to new compilation errors in code that previously used to compile, due to a name collision
(see previous).

4) Modern IDEs have accelerators, code elision and and other features that help you keep your imports under control if
you use explicit imports.

"""