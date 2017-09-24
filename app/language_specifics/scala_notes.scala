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

//to run the Main object, in sbt type `run`
>run 

>run-main com.krux.marketer.mp.pipeline.MPSegmentPipeline2 create --activate --force --name "com.krux.marketer.mp.pipeline.MPSegmentPipeline2 backfill - 2017-09-15 - Suhas - DEV-8295" --start 2017-09-16 --times 1

//submitting assignment solutions
>submit your.email@domain.com submissionPassword
//submission password for suhas.satish@gmail.com  is  YPPHnnNnDg
//Note: sbt can only be started within a project directory

------------
//in order to make the object executable (runnable) it has to extend the trait `App` or have a `main` method
import example.Lists._

object Main extends App {
	println(Lists.max(List(1,3,2)))
}

object Hello {
	def main(args: Array[String]) = println("Hello World")
}

//In order to run a Scala program, the JVM has to know the directory where classfiles are stored. This parameter is called the “classpath”.
--------------------
/*Evaluation rules */

def example = 2      // evaluated when called
val example = 2      // evaluated immediately
lazy val example = 2 // evaluated once when needed

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

class MyClass(x: Int, y: Int) {           //defines a new type MyClass with a constructor
	require(y > 0, "y must be positive")    //precondition, triggering an IllegalArgumentException if not met
	def this(x: Int) = {...}                //auxiliary constructor
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

//traits are similar to java interfaces except that they can have non-abstract members:
trait Planar {...}
class Square extends Shape with Planar  //this is like java `implements` keyword for interfaces

//general object heirarchy
scala.Any    //base type of all types, has methods `hashCode` and `toString` that can be overloaded

scala.AnyVal //base type of all primitive types like `scala.Double`, `scala.Float` , `scala.Char`, etc
List[AnyVal] = List(1, 2, a, b) //example showing single character is primitive

scala.AnyRef //base type of all reference types, alias of `java.lang.Object`, supertype of `java.lang.String`, `scala.List`
List[Any] = List(1, 2, a, bcd) //example showing group of characters becomes a String (ie object reference type and not primitive

scala.Null   // is a subtype of `scala.AnyRef`. `null` is the only instance of type `Null`
scala.Nothing //is a subtype of `scala.AnyVal` , without any instance

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

----------------------
//Collections and Data Structures

//Base Classes
Iterable (collections you can iterate on)
Seq (ordered sequences)
Set
Map (lookup data structure)


//Immutable Collections
List (linked list, provides fast sequential access)
Stream (same as List, except that the tail is evaluated only on demand)
Vector (array-like type, implemented as tree of blocks, provides fast random access)
Range (ordered sequence of integers with equal spacing)
String (Java type, implicitly converted to a character sequence, so you can treat every string like a Seq[Char])
Map (collection that maps keys to values)
Set (collection without duplicate elements)


//Mutable Collections
Array (Scala arrays are native JVM arrays at runtime, therefore they are very performant)
//Scala also has mutable maps and sets; these should only be used if there are performance issues with immutable types

//examples
val fruitList = List("apples", "oranges", "pears")
// Alternative syntax for lists
val fruit = "apples" :: ("oranges" :: ("pears" :: Nil)) // parens optional, :: is right-associative
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
List(x1, ..., xn).foldLeft(z)(op)  // (...( z op x1) op x2) op ...) op xn
List(x1, ..., xn) reduceRight op   // x1 op (... (x{n-1} op xn) ...)
List(x1, ..., xn).foldRight(z)(op) // x1 op (... (    xn op  z) ...)

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
/*Every case class has an apply and unapply method. When you construct a case class instance, you call the apply() method */
case class Currency(value: Double, unit: String)
Currency(29.95, "EUR") // Calls Currency.apply
/*
1) A case class is a class for which the compiler automatically generates the methods for pattern matching.

2) Use the Option type for values that may or may not be present — it is safer than using null.

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
TODO - what do keywords `implicit` and `sealed` mean?
*/

//------------------------------
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
//TODO: numbers every scala programmer should know - https://www.youtube.com/watch?v=AITVZISPJes
