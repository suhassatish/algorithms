/*
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
*/
//------------------------

/*
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
*/
//------------------------

/*
Java 9 notes - 
"The Big Kill Switch" to turn off encapsulation --illegal-access  

jlink: The java linker (JEP 282)
jlink --modulepath $JDKMODS --addmods java.base --output myimage

OSGI supports versioning
Implications of jlink - write once, run (test) everywhere

CMS garbage collector getting deprecated in java 9. 

can plit heap b/w non-volatile RAM and volatile RAM

Epsilon GC is a NULL GC. Useful for testing garbage collection. 

Project Valhalla - value types in Java. Identity leads to pointers -> indirection -> suffering of performance
Java has primitives for performance; Objects for encapsulation, polymorphism, inheritance, OO

ArrayList<int> wont work. ArrayList<Integer> requires boxing and unboxing.
Value types codes like a class, works like a primitive.
- can have methods and fields
- can implement interfaces

Project Panama - interconnecting JVM and native code.

Project Loom - concurrent programming made simpler. 1M threads in JVM needs vv powerful super computer.
OS thread is not light weight enough.
Have something called fibers, threads at JVM level instead of OS level. 
Has close to zero overhead for task switching. This is recreating green threads.
Use the ForkJoinPool scheduler

Project metropolis - rewrite most of the JVM in java. Use the Graal compiler project as significant input.

Can have both classpath and modulepath. 
Moving away from distinction between JDK and JRE. Idea is to now move to Jlink. There is no such thing as JRE any more. 
*/
//------------------------

//java8 : has added 2 new packages java.util.function and java.util.streams
//syntax:  (lambda parameter) -> lambdaBody
//compiler performs type inference for lambda expressions
