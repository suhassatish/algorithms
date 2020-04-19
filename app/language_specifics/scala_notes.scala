//non-determinism = result of parallel processing + mutable state
//Reduce mutable state by programing functionally. 

------
//disadvantages of spark vs grid gain (apache ignite) in-memory data fabric  - 
// 1. spark doesn't do transactions at all.
// 2. spark doesn't support in-memory indexes, joins and group-by will be slow as it has to do full scan. 
------------
sbt // this will start sbt console. scala repl (cmd-line interpreter) is bundled within sbt and can be started within sbt with the cmd `console`
>console

>compile
>test
>run
>projects // lists projects
>project <project_name> //to switch to a project
>assembly //creates a single assembly jar per project

> submit e-mail@university.org suBmISsioNPasSwoRd
sbt "submit e-mail@university.org suBmISsioNPasSwoRd"
sbt "run-main com.alvinalexander.Foo"
> run-main com.alvinalexander.Foo

//check which sbt version
sbt sbtVersion 
sbt about

//check which scala version within sbt
>console
console> util.Properties.versionString

//to run the Main object, in sbt type `run`
>run 

>last compile:runMain

>run-main com.krux.marketer.mp.pipeline.MPSegmentPipeline2 create --activate --force --name "com.krux.marketer.mp.pipeline.MPSegmentPipeline2 backfill - 2017-09-15 - Suhas - DEV-8295" --start 2017-09-16 --times 1

//submitting assignment solutions
>submit your.email@domain.com submissionPassword
//submission password for suhas.satish@gmail.com  is  YPPHnnNnDg
//Note: sbt can only be started within a project directory

------------
//in order to make the object executable (runnable) it has to extend the trait `App` or have a `main` method
import example.Lists._

object Main extends App { //older scala versions had an `Application` trait that executed the block in the static initializer which is not optimized by the JIT just-in-time compiler. Use the `App` trait instead
	println(Lists.max(List(1,3,2)))
}

object Hello {
	def main(args: Array[String]) = println("Hello World")
}

//In order to run a Scala program, the JVM has to know the directory where classfiles are stored. This parameter is called the “classpath”.
--------------------
/*Evaluation rules */

def example = 2      // evaluated when called
val example = 2      // evaluated immediately (when variable is in scope)

lazy val example = 2 // evaluated once when needed
//lazy val denotes a field that will only be calculated once it is accessed for the first time and is then stored for future reference. 
//laziness is not w/o cost. Every time a lazy val is called, a thread-safe check is performed to see if the value has been already initialized.

//--------------------------------------------------------------------------------
@transient lazy val //on the other hand one can denote a field that shall not be serialized. 
//Use case: in spark, it maybe costlier to serialize and send a field
//across a N/W cluster than it is to recompute it. Thats when you use this.  Transient fields of a serializable class will be computed at-most once per deserialization.

class Foo(val bar: String) extends Serializable {
  @transient lazy val baz: String = {
    println("Calculate baz")
    bar + " world"
  }
}

// Create object of class Foo
val foo = new Foo("Hello")

// baz field is only calculated once
foo.baz
foo.baz

// Serialize foo
import java.io._
val bo = new ByteArrayOutputStream
val o = new ObjectOutputStream(bo)
o.writeObject(foo)
val bytes = bo.toByteArray

// Deserialize foo
val bi = new ByteArrayInputStream(bytes)
val i = new ObjectInputStream(bi)
val foo2 = i.readObject.asInstanceOf[Foo]

// baz field is recalculated once and only once
foo2.baz
foo2.baz

//another application is when you have io streams which are simply not serializable. In this case you want to make sure to store the file path 
//URI to the stream so that the class can read off the stream directly and reconstruct it in-memory without having to deserialize it.
//-----------------------------------------------------------------------------------
def square(x: Double)    // call by value: evaluates the function arguments before calling the function

def square(x: => Double) //call by name: evaluates the function first, and then evaluates the arguments if need be
/*
Call-by-value has the advantage that it evaluates every function
argument only once.

Call-by-name has the advantage that a function argument is not evaluated if the 
corresponding parameter is unused in the evaluation of the function body.

for CBV and CBN to end in the same answer, a function must be all of:
a) pure
b) should terminate (ie, not inifinite loop or sequence)
----
CBV terminates => CBN terminates too, but the inverse is not true 
*/



def myFunc(bindings: Int*) {...} //bindings is a sequence of int, containing a varying # of arguments

---------------------------
/*Higher order functions : functions that take a fn as argument or return another function*/

//sum() returns a function that takes two integers and returns an integer
def sum(f: Int => Int): (Int, Int) => Int = {
	def sumf(a: Int, b: Int): Int = {...}
	sumf
}

// same as above. Its type is:
//(Int => Int) => (Int, Int) => Int  
//above line is read as: takes a function with signature `(Int => Int)` as argument and returns a function which takes `(Int, Int)` as argument and returns an Int
def sum(f: Int => Int)(a: Int, b: Int): Int = { ... } 

//called like this
sum((x: Int) => x * x * x)  //Anonymous function, ie does not have a name
sum(x => x * x * x)  //same anonymous function with type inferred
---------------------------

/* CURRYING : converting a function with multiple argumnts into a function with a single argument that returns another function*/

def f(a: Int, b: Int): Int //uncurried version (type is (Int, Int) => Int)
def f(a: Int)(b: Int): Int //curried version (type is Int => Int => Int
---------------------------
/* CLASSES */

class MyClass(x: Int, y: Int) {           //defines a new type MyClass with a primary constructor
	require(y > 0, "y must be positive")    //precondition, triggering an IllegalArgumentException if not met
	def this(x: Int) = {...}                //all auxiliary constructors are named `this`. Its a deviation from java/C++ where the class name is the constructor name which can be inconvenient if the class name is changed.
	def nb1 = x                             //public method computed every time it is called
	def nb2 = y
	private def test(a: Int): Int = { ... } //private method
	val nb3 = x + y                         // computed only once
	override def toString =									//overridden method
    member1 + ", " + member2
}

new MyClass(1, 2)  // creates a new object of type


//`this` references the current object, assert(<condition>) issues `AssertionError` if condition is not met. See `scala.Predef` for `require`, `assume`, `assert`
-----------

/* OPERATORS */

//`myObject myMethod 1` is the same as calling `myObject.myMethod(1)`

//operator ie function names can be alphanumeric, symbolic (eg x1, *, +?%&, vector_++, counter_=)

//the precedence of an operator is determined by its first character, with the following increasing order of priority: 

(all letters)
| 
^
&
< >
= !
:
+ -
* / %
(all other special characters)

//associativity of an operator is determined by its last character: right-associative if ending with `:`, left-associative otherwise
/*
https://stackoverflow.com/questions/6559996/scala-list-concatenation-vs/32135472#32135472
Because of List being singly-linked and immutable in scala, concatenating lists with ::: is better than ++ due to explanations 
above in stack overflow
*/

//note that assignment operators have lowest precedence . scala language spec 2.9 sections 6.12.3, 6.12.4 for more info
----------------------
/*Class hierarchies*/

abstract class TopLevel {     // abstract class  
  def method1(x: Int): Int   // abstract method  
  def method2(x: Int): Int = { ... }  
}

class Level1 extends TopLevel {  
  def method1(x: Int): Int = { ... }  
  override def method2(x: Int): Int = { ...} // TopLevel's method2 needs to be explicitly overridden  
}

object MyObject extends TopLevel {...} // defines a singleton object. No other instance can be created

In Scala there exists a special kind of class named case classes
Classes in Scala cannot have static members. you can use objects to achieve similar functionality as with static members in Java.

Object in Scala are like classes, but for every object definition there is only one single instance (singleton). 
It is not possible to create instances of objects using new, instead you can just access the members (methods or fields) of an object using its name.
----------------------
/* CLASS ORGANIZATION */

//different ways to import
import myPackage.MyClass
import myPackage._
import myPackage.{MyClass1, MyClass2}
import myPackage.{MyClass1 => A}

//all members of pkg  `scala` , `java.lang` , all members of object `scala.PreDef` are automatically imported

//package object in scala : If you have some helper method you'd like to be in scope for an entire package, 
//go ahead and put it right at the top level of the package.
//Each package is allowed to have one package object. Any definitions placed in a package object are considered members of the package itself.
//package objects can contain `objects`, `classes` and `traits` but not definitions of functions or variable. This is due to a JVM-limitation.

//there is no enforced relationship b/w dir of src file and pkg (package). If you have 2 files with 2 classes com.horstmann.Employee.scala and com.horstmann.Manager.scala, they dont have to exist in a com/horstmann dir structure.

//traits are similar to java interfaces except that they can have non-abstract members (like abstract classes):
//a class can 'mix-in' multiple traits 
trait Planar {...}
class Square extends Shape with Planar  //this is like java `implements` keyword for interfaces
// a trait cannot be initialized directly, but only through a class object.
//there is a short hand syntax for it
val addOne = new SimpleTrait{}  //this creates an anonymous class object

//http://www.cakesolutions.net/teamblogs/2011/12/19/cake-pattern-in-depth
//regular long-hand way of initializing a trait
class SimpleClass extends SimpleTrait
val addOne = new SimpleClass

//traits can be nested as follows - 
trait UserRepositoryComponent {
  def userLocator : UserLocator
  def userUpdater : UserUpdater  //making this def instead of val gives us flexibility in implementation with any subtype of trait UserUpdater can be returned
  trait UserLocator {
    def findAll: java.util.List[User]
  }
  trait UserUpdater {
    def save(user: User)
  }
}

//above trait is implemented as below 
trait UserRepositoryJPAComponent extends UserRepositoryComponent {
  val em: EntityManager
  def userLocator = new UserLocatorJPA(em)
  def userUpdater = new UserUpdaterJPA(em)

  class UserLocatorJPA(val em: EntityManager) extends UserLocator {
    def findAll = em.createQuery("from User", classOf[User]).getResultList
  }
  class UserUpdaterJPA(val em: EntityManager) extends UserUpdater {
    def save(user: User) { em.persist(user) }
  }
}

//----------------------------
//general object heirarchy
scala.Any    //base type of all types, has methods `hashCode` and `toString` that can be overloaded

scala.AnyVal //base type of all primitive types like `scala.Double`, `scala.Float` , `scala.Char`, etc
List[AnyVal] = List(1, 2, a, b) //example showing single character is primitive

scala.AnyRef //base type of all reference types, alias of `java.lang.Object`, supertype of `java.lang.String`, `scala.List`
List[Any] = List(1, 2, a, bcd) //example showing group of characters becomes a String (ie object reference type and not primitive

scala.Null   // is a subtype of `scala.AnyRef`. `null` is the only instance of type `Null`
scala.Nothing //is a subtype of `scala.AnyVal` , without any instance. Where there is a "throw new Exception" its type is `Nothing`

----------------------

/* TYPE PARAMETERS - similar to java generics or C++ templates - they apply to classes, traits or functions */

class MyClass[T](arg1: T) {...}
new MyClass[Int](1)
new MyClass(1) //type is being inferred based on value of arguments

//to restrict the type being used:
def myFct[T <: TopLevel](arg: T): T = { ... } // T must derive from TopLevel or be TopLevel
def myFct[T >: Level1](arg: T): T = { ... }   // T must be a supertype of Level1
def myFct[T >: Level1 <: Top Level](arg: T): T = { ... }

----------------------
/* Variance */
Given A <: B

If C[A] <: C[B], C is covariant

If C[A] >: C[B], C is contravariant

Otherwise C is nonvariant

class C[+A] { ... } // C is covariant
class C[-A] { ... } // C is contravariant
class C[A]  { ... } // C is nonvariant
For a function, if A2 <: A1 and B1 <: B2, then A1 => B1 <: A2 => B2.

Functions must be contravariant in their argument types and covariant in their result types, e.g.

trait Function1[-T, +U] {
  def apply(x: T): U
} // Variance check is OK because T is contravariant and U is covariant

class Array[+T] {
  def update(x: T)
} // variance checks fails
Find out more about variance in lecture 4.4 and lecture 4.5

def prepend[U >: T](elem: U): List[U] = new Cons(elem, this) //this works due to the rules below
/*
1) Covariant type parameters may appear in lower bounds of method type parameters

2) Contravariant type parameters may appear in upper bounds of method
*/
---------------------
Pattern Matching
Pattern matching is used for decomposing data structures:

unknownObject match {
  case MyClass(n) => ...
  case MyClass2(a, b) => ...
}
Here are a few example patterns

(someList: List[T]) match {
  case Nil => ...          // empty list
  case x :: Nil => ...     // list with only one element
  case List(x) => ...      // same as above
  case x :: xs => ...      // a list with at least one element. x is bound to the head,
                           // xs to the tail. xs could be Nil or some other list.
  case 1 :: 2 :: cs => ... // lists that starts with 1 and then 2
  case (x, y) :: ps => ... // a list where the head element is a pair
  case _ => ...            // default case if none of the above matches
}
The last example shows that every pattern consists of sub-patterns: it only matches lists with at least one element, where that element is a pair. x and y are again patterns that could match only specific types.

Options
Pattern matching can also be used for Option values. Some functions (like Map.get) return a value of type Option[T] which is either a value of type Some[T] or the value None:

val myMap = Map("a" -> 42, "b" -> 43)
def getMapValue(s: String): String = {
  myMap get s match {
    case Some(nb) => "Value found: " + nb
    case None => "No value found"
  }
}
getMapValue("a")  // "Value found: 42"
getMapValue("c")  // "No value found"
Most of the times when you write a pattern match on an option value, the same expression can be written more concisely using combinator methods of the Option class. For example, the function getMapValue can be written as follows:

def getMapValue(s: String): String =
  myMap.get(s).map("Value found: " + _).getOrElse("No value found")
-------------------------------------------------
Pattern Matching in Anonymous Functions
Pattern matches are also used quite often in anonymous functions:

val pairs: List[(Char, Int)] = ('a', 2) :: ('b', 3) :: Nil
val chars: List[Char] = pairs.map(p => p match {
  case (ch, num) => ch
})
Instead of p => p match { case ... }, you can simply write {case ...}, so the above example becomes more concise:

val chars: List[Char] = pairs map {
  case (ch, num) => ch
}

//list of tuples
val m: List[(String, String)] = List(("1", "org1"), ("2", "org2"), ("3", "org3"), ("4", "org4"))

m.map{ case (org_id, org) => (Option((org_id.hashCode % 2).toString) ,org_id + "^" + org)}
  .groupBy(_._1)
  .mapValues(_.map(_._2))
//returns Map(Some(1) -> List(1^org1, 3^org3), Some(0) -> List(2^org2, 4^org4))

----------------------
//Collections and Data Structures

//CHAPTER 13: COLLECTIONS

Iterable
  Seq
    IndexedSeq //this is super-type of Array but not of List, allows for fast random access
      Vector //immutable equivalent of ArrayBuffer
      Range
      ArrayBuffer //mutable

    List
    Stream
    Stack
    Queue
    PriorityQueue
    ListBuffer  //mutates List elements in-place

  Set  //Key methods: contains, subsetOf, union, intersect, diff
    SortedSet  //mutable
    LinkedHashSet  //mutable. Remembers order of insertion of elements
    BitSet //both immutable and mutable

  Map
    SortedMap
//to compare elements of a Seq with elements of a Set, use `sameElements` method




//Immutable Collections
List (linked list, provides fast sequential access). // List is immutable but array is mutable in scala. List stores elements recursively (in a tree-like structure) but array is flat. Both array and list elements must be of the same homgenous type unlike python lists which can be heterogenous.
Stream (same as List, except that the tail is evaluated only on demand)

Vector (array-like type, implemented as tree (not binary but a larger branching factor. Each node can hold upto 32 (2^ 5) elements) of blocks, provides fast random access)
//Because vectors strike a good balance between fast random selections and fast random functional updates, they are currently the default implementation of immutable indexed sequences in scala 2.8





Range (ordered sequence of integers with equal spacing)
String (Java type, implicitly converted to a character sequence, so you can treat every string like a Seq[Char])
Map (collection that maps keys to values)
Set (collection without duplicate elements)


//Mutable Collections
Array (Scala arrays are native JVM arrays at runtime, therefore they are very performant)

//example of appending aka concatenating to an array
def batches = Array.concat((0 to numBaseBatches - 1).toArray, (startSpecialBatches to startSpecialBatches + numSpecialBatches - 1).toArray)

//Scala also has mutable maps and sets; these should only be used if there are performance issues with immutable types

//examples
val fruitList = List("apples", "oranges", "pears")
// Alternative syntax for lists
val fruit = "apples" :: ("oranges" :: ("pears" :: Nil)) // parens optional, :: (operator is pronounced as cons) is right-associative. 
//It is also evaluated as RHS-most element making function call with the previous element as its arg, and a cascade so on. 
//Eg - Above expression is equivalent to  Nil.::("pears").::("oranges").::("apples")

List[A] ::: List[B]  //the ::: operator preprends a list to another list. This is different from the cons (::) operator in that the left argument to cons is a single item, not an iterable Seq by itself.

fruit.head   // "apples"
fruit.tail   // List("oranges", "pears")
val empty = List()
val empty = Nil

val nums = Vector("louis", "frank", "hiromi")
nums(1)                     // element at index 1, returns "frank", complexity O(log(n))
nums.updated(2, "helena")   // new vector with a different string at index 2, complexity O(log(n))

val fruitSet = Set("apple", "banana", "pear", "banana")
fruitSet.size    // returns 3: there are no duplicates, only one banana

val r: Range = 1 until 5 // 1, 2, 3, 4
val s: Range = 1 to 5    // 1, 2, 3, 4, 5
1 to 10 by 3  // 1, 4, 7, 10
6 to 1 by -2  // 6, 4, 2

val s = (1 to 6).toSet
s map (_ + 2) // adds 2 to each element of the set

val s = "Hello World"
s filter (c => c.isUpper) // returns "HW"; strings can be treated as Seq[Char]

// Operations on sequences
val xs = List(...)
xs.length   // number of elements, complexity O(n)
xs.last     // last element (exception if xs is empty), complexity O(n)
xs.init     // all elements of xs but the last (exception if xs is empty), complexity O(n)
xs take n   // first n elements of xs
xs drop n   // the rest of the collection after taking n elements
xs(n)       // the nth element of xs, complexity O(n)
xs ++ ys    // concatenation, complexity O(n)
xs.reverse  // reverse the order, complexity O(n)
xs updated(n, x)  // same list than xs, except at index n where it contains x, complexity O(n)
xs indexOf x      // the index of the first element equal to x (-1 otherwise)
xs contains x     // same as xs indexOf x >= 0
xs filter p       // returns a list of the elements that satisfy the predicate p
xs filterNot p    // filter with negated p 
xs partition p    // same as (xs filter p, xs filterNot p)
xs takeWhile p    // the longest prefix consisting of elements that satisfy p
xs dropWhile p    // the remainder of the list after any leading element satisfying p have been removed
xs span p         // same as (xs takeWhile p, xs dropWhile p)

List(x1, ..., xn) reduceLeft op    // (...(x1 op x2) op x3) op ...) op xn

List(x1, ..., xn).foldLeft(z)(op)  // (...( z op x1) op x2) op ...) op xn; short-hand for fold left is the operator /:  
//foldLeft is internally implemented as a while loop. So it works for both short and long lists. Unlike foldRight, its not implemented recursively
//For collections, prefer foldLeft instead of empty check & reduce, unless it's expensive to create a zero element. This is recommended by scala experts.
//foldLeft is not parallelizable in scala while `fold` is.
//foldLeft and foldRight API methods DO NOT exist in spark. But `reduce`, `fold` and `aggregate` are common methods in both scala and spark

List(x1, ..., xn) reduceRight op   // x1 op (... (x{n-1} op xn) ...)

List(x1, ..., xn).foldRight(z)(op) // x1 op (... (    xn op  z) ...). Accumulates results from back to front. But has some problems, so not recommended. https://oldfashionedsoftware.com/2009/07/10/scala-code-review-foldleft-and-foldright/
//foldRight is implemented recursively but not tail recursively. So for large lists, it fails with StackOverflowException. 

xs exists p    // true if there is at least one element for which predicate p is true
xs forall p    // true if p(x) is true for all elements
xs zip ys      // returns a list of pairs which groups elements with same index together
xs unzip       // opposite of zip: returns a pair of two lists
xs.flatMap f   // applies the function to all elements and concatenates the result
xs.sum         // sum of elements of the numeric collection
xs.product     // product of elements of the numeric collection
xs.max         // maximum of collection
xs.min         // minimum of collection
xs.flatten     // flattens a collection of collection into a single-level collection
xs groupBy f   // returns a map which points to a list of elements
xs distinct    // sequence of distinct entries (removes duplicates)

x +: xs  // creates a new collection with leading element x; eg - xs  = [1,2,3]; 4 +: xs  returns List(4,1,2,3)
xs :+ x  // creates a new collection with trailing element x; eg - xs = [1,2,3]; xs :+ 4 returns List(1,2,3,4)

// Operations on maps
val myMap = Map("I" -> 1, "V" -> 5, "X" -> 10)  // create a map
val m = Map[Char, Int]() //creates an empty map

val m2 = new Map[Char, Int]; //error: trait Map is abstract; cannot be instantiated 

myMap("I")      // => 1  
myMap("A")      // => java.util.NoSuchElementException  
myMap get "A"   // => res12: Option[Int] = None 
myMap get "I"   // => res13: Option[Int] = Some(1)
myMap.updated("V", 15)  // returns a new map where "V" maps to 15 (entry is updated)
                        // if the key ("V" here) does not exist, a new entry is added

// Operations on Streams
val xs = Stream(1, 2, 3)
val xs = Stream.cons(1, Stream.cons(2, Stream.cons(3, Stream.empty))) // same as above
(1 to 1000).toStream // => Stream(1, ?)
x #:: xs // Same as Stream.cons(x, xs)
         // In the Stream's cons operator, the second parameter (the tail)
         // is defined as a "call by name" parameter.
         // Note that x::xs always produces a List
-------------------------------


//Pairs (similar for larger Tuples)
val pair = ("answer", 42)   // type: (String, Int)
val (label, value) = pair   // label = "answer", value = 42  
pair._1 // "answer"  
pair._2 // 42  
----------------------

//Ordering
There is already a class in the standard library that represents orderings: scala.math.Ordering[T] which contains comparison functions such as lt() and gt() for standard types. 
Types with a single natural ordering should inherit from the trait scala.math.Ordered[T].

import math.Ordering  

def msort[T](xs: List[T])(implicit ord: Ordering) = { ...}  
msort(fruits)(Ordering.String)  
msort(fruits)   // the compiler figures out the right ordering  
----------------------
//For-Comprehensions
A for-comprehension is syntactic sugar for map, flatMap and filter operations on collections.

The general form is for (s) yield e
s is a sequence of generators and filters
p <- e is a generator
if f is a filter
If there are several generators (equivalent of a nested loop), the last generator varies faster than the first
You can use { s } instead of ( s ) if you want to use multiple lines without requiring semicolons
e is an element of the resulting collection

//example
val result = for {
  user             <- UserService.loadUser("mike")
  usersChild       <- user.child
  usersGrandChild  <- usersChild.child
} yield usersGrandChild

----------------------
//Example 1
// list all combinations of numbers x and y where x is drawn from
// 1 to M and y is drawn from 1 to N
for (x <- 1 to M; y <- 1 to N)
  yield (x,y)
is equivalent to

(1 to M) flatMap (x => (1 to N) map (y => (x, y))) //this is a confusing syntax, to be avoided
----------------------

//Translation Rules
A for-expression looks like a traditional for loop but works differently internally

for (x <- e1) yield e2 is translated to e1.map(x => e2)

for (x <- e1 if f) yield e2 is translated to for (x <- e1.filter(x => f)) yield e2

for (x <- e1; y <- e2) yield e3 is translated to e1.flatMap(x => for (y <- e2) yield e3)

This means you can use a for-comprehension for your own type, as long as you define map, flatMap and filter.

For more, see lecture 6.5.
----------------------

//Example 2
for {  
  i <- 1 until n  
  j <- 1 until i  
  if isPrime(i + j)  
} yield (i, j)  
//most readable
is equivalent to

for (i <- 1 until n; j <- 1 until i if isPrime(i + j))
    yield (i, j)  
//moderately readable
is equivalent to

(1 until n).flatMap(i => (1 until i).filter(j => isPrime(i + j)).map(j => (i, j)))  //confusing syntax, least readable

--------------------------
//scala style guide
1) Never use isInstanceOf or asInstanceOf - there’s always a better solution. 
so avoid Casts and Type tests

2)Semicolons in Scala are only required when writing multiple statements on the same line. 
writing unnecessary semicolons should be avoided

3) avoid using Return statement. You dont need explicit returns because control structures like If are expressions. 
def factorial(n: Int): Int = {
	if (n <=0) 1
	else (n * factorial(n-1))
}

//notice that there are no return statements above


4) avoid Mutable Local Variables. you can always write code that uses mutable local variables to code with Helper Functions that take Accumulators

eg - for fibonacci sequence, the preferred way to write it functionally is as follows instead of using local variables that are primitive Ints

def fib(n: Int): Int = {
	def fibIter(n: Int, a: Int, b: Int): Int =
		if (i==n) a else fibIter(i+1, b, a+b)
	fibIter(0, 0, 1)
}

5) avoid redundant If statements
eg - instead of 
if (cond) true else false
you can write 
cond
------------------------------
//functional of of implementing `and` operator without using && 
def and(x: Boolean, y: => Boolean): Boolean = if(x) y else false
--

//Recursive functions need an explicit return type in Scala.
//For non-recursive functions, the return type is optional
/*to find the sqrt of a number using newton's method of successive approximation , 
where sqrt(x) is found by starting with y= 1 & repeatedly seeing if x/y ~= y & ,
then refining y by new_y = mean(y + x/y).
Scala implementation follows:
 */

def sqrtIter(x: Double, y: Double) : Double = 
  if isGoodEnough(x, y) y
  else sqrtIter(x, getRefinedY(x, y))

def isGoodEnough(x: Double, y: Double) : Double
  abs((x/y) - y) / x <= 0.001

def getRefinedY(x: Double, y: Double) : Double = 
  (x/y + y)/2

def sqrt(x: Double) = srqtIter(x, 1.0)
//-------------------------------------

/*
Every case class has an apply and unapply method. When you construct a case class instance, you call the apply() method, which mimics a constructor 
unapply() method mimics an extractor which is required to be implemented under-the-hood for pattern matching with case statements to work.

Case classes are special because scala automatically creates a companion object for them with an apply() and unapply() methods.

.*/
case class Currency(value: Double, unit: String)
Currency(29.95, "EUR") // Calls Currency.apply
/*
1) A case class is a class for which the compiler automatically generates the methods for pattern matching.

2) Use the Option type for values that may or may not be present — it is safer than using null.
Using pattern matching on Option is not idiomatic in scala. Instead, just use Option[Int].getOrElse("default value")

3) Scala has an abstract class Enumeration which provides a light weight alternative to `case classes`. Each call to the `Value` method
adds a new unique value to the enumeration.
*/ 

object WeekDay extends Enumeration {
  type WeekDay = Value
  val Mon, Tue, Wed, Thu, Fri, Sat, Sun = Value
}
import WeekDay._

def isWorkingDay(d: WeekDay) = ! (d == Sat || d == Sun)

WeekDay.values filter isWorkingDay foreach println
//-----------------------------------------
//to try scala REPL with imports within a scala repo, start the scala REPL within the repo by setting the classpath as below.
//Then scala will start recognizing the imports of the repo
scala -classpath marketer-analytics/target/scala-2.11/classes/:/Users/ssatish/.ivy2/cache/org.json4s/json4s-jackson_2.11/jars/json4s-jackson_2.11-3.2.11.jar:/Users/ssatish/.ivy2/cache/org.json4s/json4s-core_2.11/jars/json4s-core_2.11-3.2.11.jar:/Users/ssatish/.ivy2/cache/org.json4sjson4s-ast_2.11/jars/json4s-ast_2.11-3.2.11.jar

//to paste multiple lines into scala REPL (like in ipython)
scala> :paste
// Entering paste mode (ctrl-D to finish)

//------------------------------
/*
what does keyword `sealed` mean?

Sealed - When using patttern matching with case classes, if abstract superclass is declared as sealed, compiler exhaustively checks for all alternatives.
*/
sealed abstract class Amount
case class Dollar(value: Double) extends Amount
case class Currency(value: Double, unit: String) extends Amount
//all case classes extending from an abstract sealed class should be in the same file, since compiler needs to know about it at compile time

//------------------------------
//keyword implicit : implicit function is defined with a single parameter.
implicit def int2Fraction(n: Int) = Fraction(n, 1)

val result = 3 * Fraction(4, 5) // calls int2Fraction(3)

//an implicit class must have a primary constructor with exactly 1 argument.
implicit class RichFile(from: File) extends AnyVal
//in the above example, you can enrich the `File` class with `RichFile` implicit class which has an added `read` method thats missing in the `File` class.
//by making it extend `AnyVal`, no `RichFile` objects are created. A call `file.read` is directly compiled into a static method call `RichFile$.read$extension(file)`


//--------------------------------
/*unit tests in scala
http://www.scalatest.org/user_guide/writing_your_first_test
*/
scalac -cp scalatest-app_2.11.7-3.0.1.jar StackSpec.scala
scala -cp scalatest-app_2.11.7-3.0.1.jar org.scalatest.run StackSpec

//to run a single unit test in sbt (dont have to worry about classpath)
> testOnly *MPSegmentPipelineRerunTest
/* ~~~~~~~~~~~~~~~ REACTIVE CHEAT SHEET ~~~~~~~~~~~~~~~~*/

//PARTIAL FUNCTIONS
a subtype of Trait Function1 that is well defined on  a subset of its domain
trait PartialFunction[-A, +R] extends Function1[-A, +R] {
	def apply(x: A): R
	def isDefinedAt(x: A): Boolean
}

every concrete implementation of PartialFunction has the usual `apply` method along with a boolean method `isDefinedAt`
------------------------
//numbers every scala programmer should know - https://www.youtube.com/watch?v=AITVZISPJes - Hunter Payne, Credit Karma
/*
Operation                                   |Time                 |Exponent (order of time)
Generate random number                      | 25 ns               | 1
Get current time                            | 50 ns               | 1
Match against 6 cases using Class           | 150 ns              | 2
Match against 6 cases using Integer         | 150 ns              | 2
Constructing a Case Class with 4 args       | > 400 ns (~1600 ns) | 2
Change file attributes (ie update fs inode) | 1300 ns             | 3
Delete file (ie delete fs inode)            | 1350 ns             | 3 
Context switch                              | 1100-4500 ns        | 3 
Lookup value in map with 65536 elements     | 4,750 ns            | 3
Search an array with 65536 eleements        | 158,000 ns          | 5
Search a list with 65536 elements           | 340,000,000 ns      | 8

Upto 500 elements, use Array. Map is faster for > 500 elements. Seq data structure is the slowest.

Immutable remove is faster. Mutable is 30% faster for other operations.
*/

superclasses are fully initialized before subclasses;
when a `val` is overridden, its not ;

https://youtu.be/po3wmq4S15A
//Functional programing with effects: Rob Norris 
/*
Notes from talk above:
https://medium.com/@sinisalouc/demystifying-the-monad-in-scala-cc716bb6f534
Monad: Option (construct to avoid null pointers in scala) and Future (wrapper over some async ops) are 2 monads in scala. 
Monads are wrappers with 2 functions defined on them, ie 
  i) unit() ie identity-function that creates a monad M[A] from an object of type A. eg - apply()
  and 
  ii) flatMap() ie binding-function 
  that obey the properties:
  
    a) left-identity law: 
    unit(x).flatMap(f) == f(x)

    b) right-identity law: 
    m.flatMap(unit) == m

    c) associativity law:
    m.flatMap(f).flatMap(g) == m.flatMap(x => f(x).flatMap(g))


1) Every expression is either referentially transparent or is a side-effect. Its 1 or the other.

`identity` is also a keyword in scala that accepts and returns the same value.

----------
Tail recursion in scala: 
If a function calls itself as its last action, the function's stack frame can be reused. This is called tail recursion.
Tail recursive functions are iteratice processes.
only directly recursive calls to the current function are optimized. 
using @tailrec annotation, one can require that a dunction is tail-recursive. 


--------------------
SCALA TODO:
  a) http://danielwestheide.com/blog/2012/11/21/the-neophytes-guide-to-scala-part-1-extractors.html (part 1 is done. part 2 onwards)
  b) redbook for scala
  //https://www.scala-exercises.org/fp_in_scala/getting_started_with_functional_programming
  //exercises from the red book

  c) http://twitter.github.io/effectivescala/

  d) http://twitter.github.io/scala_school/ 
  From 0 to distributed_service
  
  e) "https://people.mpi-sws.org/~dreyer/tor/papers/wadler.pdf"
*/
----------------------------
//A value declared with `val` is actually a constant—you can’t change its contents:
//To declare a variable whose contents can vary, use a `var`

// =:= is an operator used to restrict types beyond whats defined in class generic definition. This constraint is enforced at compile-time
case class Foo[A](a:A) { // 'A' can be substituted with any type
    // getStringLength can only be used if this is a Foo[String]
    def getStringLength(implicit evidence: A =:= String) = a.length
}

//example usages below show that getStringLength can only supply the implicit value when A is a `string` type
scala> Foo("blah").getStringLength
res6: Int = 4

scala> Foo(123).getStringLength
<console>:9: error: could not find implicit value for parameter evidence: =:=[Int,String]

A =:= B means A must be exactly B
A <:< B means A must be a subtype of B (analogous to the simple type constraint <:)
A <%< B means A must be viewable as B, possibly via implicit conversion (analogous to the simple type constraint <%)
----------------------------
Scala Transformers are `map`, `filter`, `flatMap` that return a collection. Analogous equivalent in spark is a `transformation` that returns an RDD and are computed "lazily".

Scala Accessors are `fold`, `reduce`, `aggregate` that return a single value instead of a collection. In spark, analogous of accessor is `action`. They are "eagerly" computed and stored to
external storage like HDFS.

`aggregate` is parallelizable and its possible to change the return type. In this way, it gives you the best of both worlds - foldLeft (not parallelizable but can change return type) and 
fold (parallelizable but cannot change return type). If you have to change the return type of your reduction in spark, the only option is aggregate.

----------------------------
implicit class RichTry[+T](val t: Try[T]) extends AnyVal {
    def printError: Unit = t match {
      case Failure(e) => e.printStackTrace()
      case v =>
    }
  }

Try(1/0).printError

----------------------------
def unapplySeq(object: S): Option[Seq[T]]
//allows pattern matching of _* ie variable number of arguments. DanielWest Heide blog part 2
//eg below
object GivenNames {
  def unapplySeq(name: String): Option[Seq[String]] = {
    val names = name.trim.split(" ")
    if (names.forall(_.isEmpty)) None else Some(names)
  }
}
//unapply usually should return an Option of Some((tuple1, tuple2, ...tuplen))
//unapply can also return a Boolean if it doesnt extract any value as shown below
object isCompound {
  def unapply(input: String) = input.contains(" ")
}

name match {
  case Name(first, isCompound()) => ... //names like van der Linden
  case Name(first, last) => ...
}

----------------------------
//a "procedure" is a function in scala that returns a "Unit" and without an `=` assignment thats called just for its side effect.
def box(s: String) {
  val border = "-" * (s.length + 2)
  print(f"$border%n|$s|%n$border%n")
}
/* box("suhas") returns below 
-------
|suhas|
-------
*/

----------------------------
//consider using the scala-ARM lib (http://jsuereth.com/scala-arm/) for File handling, similar to the try-with-resources java statement
import resource._
import java.nio.file._
for(
  in <- resource(Files.newBufferedReader(inPath));
  out <- resource(Files.newBufferedWriter(outPath))
  ) { ... }

-----------
//the Try class is designed for failure. If an exception occurs, `Failure` object is returned, else a `Success` object is returned
import scala.io._
import scala.util.Try
val result = 
  for (
    a <- Try { StdIn.readLine("a: ").toInt };
    b <- Try { StdIn.readLine("b: ").toInt } 
  ) yield a/b
-------------
//java equivalent of resizing ArrayList is scala.collection.mutable.ArrayBuffer
//we can sort an Array in-place but not an ArrayBuffer

//difference b/w java array and scala array 
/*
java automatically converts an  Array[String] passed in function arguments to its super-type ie Array[Object] but scala doesnt since its not type safe

val a = Array("mary", "had", "a", "little", "lamb")

someFunction(a.asInstanceOf(Array[Object]))  //assume here that `someFunction`'s declaration takes in an Array[Object] as argument
*/

-------------

//java.util.ProcessBuilder has a constructor that takes a List<String>. Here's how to call it from scala
import scala.collection.JavaConversions.bufferAsJavaList
import scala.collection.mutable.ArrayBuffer

val cmd = ArrayBuffer("ls", "-al", "/home/cay")
val pb = new ProcessBuilder(cmd) //scala to java implicit conversion due to presence of bufferAsJavaList among imports
--
//conversely, when java method returns a `List`, it can be implicitly converted to scala ArrayBuffer with
import scala.collection.JavaConversions.asScalaBuffer
import scala.collection.mutable.Buffer
val cmd : Buffer[String] = pb.command() // Java to Scala
-------
//LinkedHashMap gives keys in a Map in insertion order
//scala doesnt provide a mutable TreeMap (only immutable HashMap and TreeMap & mutable (Hash) Map), so if you need mutable TreeMap, have to interoperate
//with the java version
import scala.collection.JavaConversions.mapAsScalaMap
val scores: scala.collection.mutable.Map[String, Int] = new java.util.TreeMap[String, Int]

import scala.collection.JavaConversions.propertiesAsScalaMap
val props: scala.collection.Map[String, String] = System.getProperties()

import scala.collection.JavaConversions.mapAsJavaMap
import java.awt.font.TextAttribute._ // Import keys for map below
val attrs = Map(FAMILY -> "Serif", SIZE -> 12) // A Scala map
val font = new java.awt.Font(attrs) // Expects a Java map
--------
//BELOW NOTES FROM SCALA FOR IMPATIENT CHAPTER 5 : CLASSES

//to peek into the disassembly of compiled bytecode of a JVM class within scala REPL
scala> :javap -private <ClassName>

//object-private fields
class Counter {
  private var value = 0  //scala generates private getter and private setter for this private field. 
  //Private setter in the JVM looks like public void value_$eq(int).
  //programer can also provide the setter method `private def value_ =` 

  private[this] var value2 = 1  // scala doesnt even generate any private getter or private setter. most restrictive access privilege

  private val x = 3 // has only private getter generated

  def increment() { value += 1 }

  def isLess(other: Counter) = value < other.value
  //can access private field of other object
  
  def isLess2(other: Counter) = value2 < other.value2  //throws error "value2 is not a member of Counter"
}

//to make the primary constructor private, use this syntax
class Person private(val id: Int) { ... }
//a class user then use an auxiliary constructor to construct a Person object

//timeit method in scala in REPL
bash$> scalac Hello.scala
bash$> scala -Dscala.time Hello
----------------------------------

//important difference with java inheritance : only the child class' primary constructor can call super on the parent's primary constructor
//debug construction order problems with the "-Xcheckinit" compiler flag.
------------------
/*
multiple inheritance in scala possibly with traits. When a class mixes in multiple traits, the order matters 
— the trait whose methods execute first goes to the last.

When you extend a class and then change the superclass, the
subclass doesn't have to be recompiled because the virtual machine understands
inheritance. But when a trait changes, all classes that mix in that
trait must be recompiled.
*/
-----------------------
//dynamic invocation: ORMs (ruby on rails, etc) do DB-table-CRUD-ops on objects using dynamic invocation. This can also be done in scala.
//eg - people.find(last_name = "satish") etc can be done in scala by extending the `Dynamic` trait . 
//For more details, see the end of Scala for the Impatient Chapter 11 on Operators
//Caveat: like operator overloading, dynamic invocation (skips compile-time type checks) is a feature that is best used with restraint

-----------------------------------
//CHAPTER 12 : scala4Impatient : higher-order-functions
//FUNCTIONS VS METHODS
def fun = ceil _ //the `_` tells to convert the method `ceil` which has a signature (Double)Double, without a `=>` into a function with signature (Double) => Double, 
//ie, from without an arrow to with an arrow
//in scala, you cannot manipulate methods, only functions.

//anything defined with the keyword `def` is a method, not a function
----
val f: (String, Int) => Char = _.charAt(_) //here the 1st `_` is the 1st argument of type String and 2nd `_` is a 2nd argument of type Int

//alternatively it can also be written as 
val f = (_ : String).charAt(_ : Int) // but its less readable and the return type is not obvious unless you peek into the charAt API. So above way is better
----
//closure: function inside a function
def mulBy(factor: Double) = (x: Double) => factor * x
val double = mulBy(2)
val half = mulBy(0.5)


//currying : process of converting a function that takes 2 arguments into a function that takes 1 argument. That function returns a function that consumes the 2nd argument
val mul = (x: Int, y: Int) => x * y

val mulOneAtATime = (x: Int) => ((y: Int) => x * y)

mulOneAtATime(6)(7) //this is how you call it

def mulOneAtATime(x : Int)(y : Int) = x * y // short cut syntax using `def` for defining curried functions
-----------------------------------
//Partial Functions : a set of case clauses enclosed in {} 
val f : PartialFunction[Char, Int] = { case '+' => 1 ; case '-' => 0}
//note that in PartialFunction[A, B], A is the parameter type and B is the return type
//in the above case, Char is the parameter type and Int is the return type

-----------------------------------
//annotations add data to the java byte code that can be harvested by external tools. junit, jpa and other java framework annotations can be used in scala, but scala
//annotations cannot be understood by java frameworks.

-----------------------------------
// Note from Databrick's guide book - Data Scientist's Guide to Apache Spark - mainly focusing on SparkML 

// In SparkML (MLLib uses RDDs vs sparkML uses DataFrame APIs), when you call an algorithm.fit(...), evaluation is always EAGERLY performed, launching spark jobs immediately.
val Array(trainingDF, testDF) = df.randomSplit(Array(0.7, 0.3))

import org.apache.spark.ml.classification.logisticRegression
val lr = new LogisticRegression()
  .setLabelCol("label")
  .setFeaturesCol("features")

val fittedLR = lr.fit(trainingDF) //eagerly launches spark jobs
fittedLR.transform(trainingDF).select("label", "prediction").show() //make predictions with the `transform` method


//important NOT to reuse instances of transformers, models and estimators across DIFFERENT pipelines. Always create a new instance of a model before creating another
//pipeline.
-----------------------------------
Every monad is a functor. But free monad of a functor is not the same functor as the functor you started with. Free monad is a recursive structure.
A functor is something with a map() function
--------------
//working example of reflection in scala 
val y = 5
val foo = (x: Int) => x + 1 + y
println(foo.getClass.getName)
val c = foo.getClass.getClassLoader.loadClass(foo.getClass.getName)
val m = c.getMethod("apply", classOf[Object])
println(m.invoke(foo, 1.asInstanceOf[Object]))
----------
g /usr/local/etc/sbtopts
//setup global versio of sbt in this file
------------
cd ~/git/einstein/suggested-articles2/datagen/smarticle
sbt package
for einstein suggested article smart agent repo

if sbt 0.13 and 1.0 incompatibility errors show up, delete all target folders and re-compile
cd ${your_project}
rm -fr project/target
rm -fr project/project/target
-------------------------------------
//NOTES FROM FUNCTIONAL SCALA - John DeGoes
//https://github.com/jdegoes/functional-scala

//types exist only at compile-time. Types erasure happens after JVM byte-code is generated.
//methods, pkgs ,types, statements are not values in scala. Cant assign them into a val.
val foo = (i : Int) => bar(i)
def bar(i: Int) = ???

//AlgebraicDataTypes are composed of sums and products of other types. Very important in creating data abstractions. 
//scala 2 has limitation of 22 elements in a tuple. Thats going away in scala3.

//sealed traits are how you give names in scala to a sum type. If its not sealed, its not a sum type
sealed trait CoffeePreference
case object Black extends CoffeePreference
case object WithCream extends CoffeePreference
case object WithSugar extends CoffeePreference
case object WithSugarAndCream extends CoffeePreference
case object Both(l : CoffeePreference, r: CoffeePreference) extends CoffeePreference

//scala 3 has the concept of enums instead of sealed traits to represent sum types

//unions can be opened or closed. Open unions are not sum types (trait thats not sealed). Closed unions are sum types. 

//you should never extend case classes.

//scala compiler has a problem of breaking binary compatibility, and due to that, instead of sealed trait, production code should use sealed class
-----------
domain => range
aka domain => co-domain

you can make a fn a lambda or closure and assign it to a val.
all functions `f: A => B` satisfy the following properties:
  1) totality: if a: A, then f(a) : B
  2) determinism: If a: A and b:A and a == b then f(a) == f(b)
  3) purity: The only effect of evaluating f(x) is computing the return value.

-------
recommend using scalaz subset of scala. There are tools to enforce that subset. 
There are no reflections at runtime, no nulls, etc in scalaz
--------
kotlin doesnt have higher-kinded types which is supported by scala. These allow you to abstract to another level.
List[A] is a higher-kinded type.

kinds can be regarded as a type of types. 
// Int  : *
//List : * => *
// Option : * => *
// Future : * => *
// Try : * => *
//Kind: type constructors :: value : types

//[*, *] => *, ie a type constructor that takes two type parameters
//ex = {Map, Either, Tuple2, Product2, ...}
trait Algorithm[Container[_]] {
  def runAlgorithm[A](container: Container[A]): Int = ???
}

val listAlgorithms: Algorithm[List] = ???


//partial functions - used to adapt functions that have the wrong number of parameters.
val plus: (Int, Int) => Int = (a, b) => a + b
val list: List[Int] = 1 :: 2 :: 3 ::4 ::5 :: Nil

val increment: Int => Int = plus(1, _)
list.map(plus(1, _))
list.map(increment)

//partial application of higher-kinded types
type MapString[A] = Map[String, A]
val mapSized: Sized[Map[String, _]] = ???

TODO - day 1 -  exercise 9, 10, 11 as prereq for day2
---------
If you created datatype DT but not type class TC, put implicit in companion object of TC.
https://leanpub.com/fpmortals
https://typelevel.org/blog/2016/08/21/hkts-moving-forward.html
https://medium.com/bigpanda-engineering/understanding-f-in-scala-4bec5996761f
-------
DAY 2 - 
NOTES FROM FUNCTIONAL SCALA - John DeGoes
while merging 2  maps, if V is a semigroup, Map[K, V] is a semigroup. For same keys, the values can be merged (reduced) if V is a semi-group.

Semigroup has an append() method. It is associative. It doesnt always have to combine things. eg - max semigroup.

every monoid[A] also implies a Semigroup[A]
//2 rules whether you append 0 to `a` on left or right , doesnt matter.
//eg - list concatenation; integer addition with 0; integer multiplication with 1. 

a commutative monoid has `append`, and `0`. application - mutiple google accounts. doenst matter which account you sign into first. 
---
Functor heirarchy is one of abstractions.
Functor is type classed.  Type constructor of kind * -> *
trait Functor[F[_]]

Functor[Int] will get a kind error from scala compiler.
Functor[List[Int]] works.

It has a single method called `map()`

It satisfies 2 laws - 
1) identity law
2) composition law

Functors compose very well. Product of 2 functors is a functor. 
Sum of functors is also a functor.
----------
common examples of functors are List, Future, Option  and their sum of 2 entities are as follows - 
List - Nil or Cons
Future - Success or Failure
Option - Some or None

Functor gives us the capability to turn all `RETURN a` instructions into `RETURN f(a)`
--------
next step up the functor heirarchy is apply.

`?` symbol is exactly like _ for values, but its for types. 

trait Apply[F[_]] extends Functor[F] {
  def ap[A, B](f: F[A => B])(fa: F[A]): F[B]

  def zip[A, B](fa: F[A], fb: F[B]): F[(A, B)]

}
-------------------
next step up is the Applicative in the functor heirarchy. 
It adds def point. An ordinary `A` value in scala and lift it up into a return value F[A]

trait Applicative[F[_]] extends Apply[F] {
  def point[A](a: => A): F[A]
}
eg - list.apply, future.success
---------------
monad has a capability called bind 

trait Monad[F[_]] extends Applicative[F] {
  def bind[A, B](fa: F[A])(f: A => F[B]) : F[B]
}
//context-sensitive sequential operations can be represented as monads.

//traverse is a more powerful traversable. you can do effectful for-loops with it. 
//traverseImpl() is what you have to implement, everything else comes for free.

// |@| is the symbol for zip() in scalaz library
// |+| is the symbol for append() in scalaz library

//Optics is a technique where you can modify deeply nested data structures like traverse, with ease.
---------------
trait Traverse[F[_]] extends Foldable[F] with Functor[F] {
  def traverseImpl[G[_]: Applicative, A, B](fa: F[A])(f: A => G[B]): G[F[B]]
}
//you get a sequence for free with this, which lets you take an option of lists and convert it into a list of options

//*********************----------
//CHEAT SHEET - 
object reference {
  // Associatively combines two values of type A
  trait Semigroup[A] {
    def append(l: A, r: => A): A
  }
  // Adds a zero that doesn't change values
  trait Monoid[A] extends Semigroup[A] {
    def zero: A
  }
  // Maps the return values of programs
  trait Functor[F[_]] {
    def map[A, B](fa: F[A])(f: A => B): F[B]
  }
  // Combines two programs and preserves both of their
  // return values (in a tuple):
  trait Apply[F[_]] extends Functor[F] {
    def zip[A, B](fa: F[A], fb: F[B]): F[(A, B)]

    final def ap[A, B](fab: F[A => B])(fa: F[A]): F[B] =
      map(zip(fab, fa))(t => t._1(t._2))
  }
  // Lifts an `A` value into an `F` program that just returns it.
  trait Applicative[F[_]] extends Apply[F] {
    def point[A](a: => A): F[A]
  }
  // Composes a program that returns an `A` with a function
  // that, given the A, will return another program that
  // returns a B.
  trait Monad[F[_]] extends Applicative[F] {
    def bind[A, B](fa: F[A])(f: A => F[B]): F[B]
  }
  // Folds over elements of a data structure.
  trait Foldable[F[_]] {
    def foldRight[A, Z](fa: F[A])(f: (A, Z) => Z): Z
    def foldMap[A, B: Monoid](fa: F[A])(f: A => B): B
  }
  // Effectfully loops over element of a data structure,
  // collecting the results of those effects back into the
  // same type of data structure.
  trait Traverse[F[_]] extends Foldable[F] with Functor[F] {
    def traverseImpl[G[_]: Applicative, A, B](
      fa: F[A]
    )(f: A => G[B]): G[F[B]]
  }
}

https://typelevel.org/cats/nomenclature.html
//*************

//DAY 3 - John A De Goes 
Lens[S, A] //ex - S is Person object, A is Int, like age of Person
/* 2 things  
1) we can retrieve an A from S
  get : S => A
2) functional set an A in an S where
  set : A => S
---
If S is not a Product type, but a Sum type. 
eg - If S is City where you live in,
*/
Prism[S, A]
/*
If there are 100 cities, we need 100 Prisms.
1) get: S => Option[A]
2) set: A => S
*/

These are the 3 core optics types - 
1) term & product
2) term & sum
3) term & collection
---------------------
Fibers are light weight threads . Start with no stack, then it can dynamically grow, more than 1 MB limit of that of a thread.
Overhead of fiber is much lesser , so can get to 100K or 1M fibers, much more than 10K limit of threads.

Give massive scalability, bunch of fibers share a thread. Fibers dont block. They suspend and stop until data is available.
Using ZIO, you can easily build concurrent apps.
No longer have to think about locks and threads. Write declarative code.
Lazy computation of results - if you want to run bunch of Futures in parallel, Future.firstSuccessOf() will pick the 1st winner while the others keep wasting resources.

what happens with Future if you sequence(List[Future]) ? If 1 of them fails, it returns a failure . The other 99 ones keep running, consuming resources.

So Future is extraordinarily wasteful. ZIO is on the other end of the spectrum, very lazy. 100 things in parallel in ZIO , 1 succeeds, others are all cleaned up 
immediately.

Try..Finally works for synchronous code, but not designed to work with callbacks, ie asynchrounous code. 
ZIO gives you that Try..Finally that works across asynchronous resources. Runs finalizers in reverse linear order. So there are strongest guarantees possible. 
Modern apps are mostly async. So you need Try..Finlally that works with async to clean up your resources.


*> this is called fish operator in scalaz.zio library and works sequentially

//JVM thread blocking vs Fiber suspending
//JVM threads consume resources - OS rsrcs, memory. When Fiber suspends, none of that overhead. A thread that blocks forever will consume rsrcs forever,
//but a fiber may be GCd if its not referenced. Its trivial to leak threads, but its much harder to leak fibers. 

//finalizers should never throw exceptions or fail with errors.  (in finally block)
//https://gitter.im/jdegoes/functional-scala
//TODO https://www.youtube.com/watch?v=y_QHSDOVJM8
// https://github.com/jdegoes/functional-scala
---------------
//community-einstein-with-dependencies
gradle clean
gradle jar //this target should exist in build.gradle as a json key
---------------

// scala console shell REPL multi line testing - 
"/opt/input/data/training/(.+(?=\\/))(\\/)(.+(?=\\.))(.avro)".r.findAllMatchIn("/opt/input/data/training/1ccb-salesforce/ai/dev/00DR0000000ATM0MAO/feb600a2-3bfc-431b-b410-365bbedd87e1/part-00067.avro").size

---------------
// https://stackoverflow.com/questions/20466546/getting-the-parameters-of-a-case-class-through-reflection
def caseMap[T: TypeTag: reflect.ClassTag](instance: T): List[(String, Any)] = {
  val im = rm.reflect(instance)
  typeOf[T].members.collect {
    case m: MethodSymbol if m.isCaseAccessor =>
      val name  = m.name.toString
      val value = im.reflectMethod(m).apply()
      (name, value)
  } (collection.breakOut)
}
---------------
//scala RuntimeException e
e.toString = scala.MatchError: blah (of class java.lang.String)
e.getMessage = blah (of class java.lang.String)
e.getCause = empty line \n and then the rest of the stack trace
