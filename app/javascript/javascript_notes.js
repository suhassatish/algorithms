//d3 scales color pickers - hex codes with svg library - colorpicker.com

-----------------
//fill, stroke, stroke width can be applied thru CSS.

//they are svg library's html tags.

----------
//google fonts - gives you css, html code for various templates

----------------
//inbuilt function to parse strings as floats




//also short hand for same above is overloaded + operator -

var myString = "5";
var myNumber = parseFloat(myString);
console.log(myNumber)
var myParsedNumber = +myString;
-------------------

var myArray = [1, 2, 3];

myArray[0], myArray[myArray.length -1]

var myObject = {
	x: 5,
	y: 10
};

myObject.x
myObject["y"]

var arrCopy = myArray.slice()
----------
//javascript functions -

var square = function square(x) {
	return x*x;
}
//if theres no return statement in a function, the default return value is `undefined` (like `None` in python)
//object is a collection of properties with name and value. Value cannot be `undefined`. Name can be any string including empty string.

console.log(square(5));

//functions are first-class objects;

---------
//to invoke a function on every element of an array -

var myArrayOfObjects = [
        { x: 100, y: 100},
        { x: 130, y: 120},
        { x: 80 , y: 180},
        { x: 180, y: 80 },
        { x: 180, y: 40 }
      ];

      myArrayOfObjects.forEach(function (d){
        console.log(d.x + ", " + d.y);
      });
-----------
//loading a csv file with d3.js  (all values parsed as strings)-

<html>
  <head>
    <meta charset="utf-8">
    <title>D3 Example</title>
    <script src="//cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"></script></meta>
  </head>
  <body>

    <script>
      d3.csv("data.csv", function (myArrayOfObjects){
        myArrayOfObjects.forEach(function (d){
          console.log(d.x + ", " + d.y);
        });
      });
    </script>

  </body>
</html>
//--------------------

//to parse numerical values from csv with d3.js -

      d3.csv("data.csv", type, function (myArrayOfObjects){
        myArrayOfObjects.forEach(function (d){
          console.log(d.x + d.y);
        });
      });

      function type(d){
        d.x = +d.x;
        d.y = +d.y;
        return d;
      }
//-------------------
//method chaining in javascript -
// without a semicolon, following functions are on the object returned by the first function call.


//implicit getter - function call without arguments

//implicit setter- function call with arguments

//-----

d3.scale.linear() - //domain = data space, range = pixel space;


d3.scale.ordinal() 
 .domain(["A", "B", "C"])
 .rangePoints([0, 100]) ; 
 .rangeRoundPoints(...)

console.log(scale(A))

----------
var svg = d3.select("body").append("svg"); 

//-----------
//when no DOM element exists but data exists, enter() method is called which creates the dom  in subsequent chained methods in example
// below -

//here rect is a dom which doesnt exist in the first call to be selected, but still enter() will create it in the append.


      svg.selectAll("rect")
          .data(data)
        .enter().append("rect")
          .attr("x", scale)
          .attr("y", 50)
          .attr("width",  20)
          .attr("height", 20);


//enter() doesnt update existing DOM elements, it only creates new ones if they dont exist previously.

------------------------------------------
/*
d3 has 3 phases of visualization - 
1) enter 2) update 3) exit
*/
-----------------------

//d3.extent, d3.min, d3.max
-----------------

//to debug with breakpoints in javascript code, like python ipdb.set_trace(), add the following in the code - 
debugger;

//list of keywords in javascript
/*
abstract
boolean break byte
case catch char class const continue
debugger default delete do double
else enum export extends
false final finally float for function
goto
if implements import in instanceof int interface
long
native new null
package private protected public
return
short static super switch synchronized
this throw throws transient true try typeof
var volatile void
while with
*/

//-----------------------------

/*
aura templates will be fetched from server and cached in ADS (aura data service) cache, triggering a browser background refresh. 
Its a singleton shared cache of record data across components.

 * - $Record GVP (GlobalValueProvider) acts as the server communication layer. It's required for server-initiated
 *   record loading due to its server-accessible nature. Client-initiated record loading could
 *   done by any component but $Record GVP was chosen for consistency and code re-use.
*/


//Using closures for private variables makes debugging a hassle.
//The function object nested inside another function, and assigned to a var like,
function outer_func() {
  var a = function inner_func() {

  }
}
//inner_func() contains a link to that outer context. This is called closure. This is the source of enormous expressive power.
//every function also gets 2 hidden parameters along with the arguments passed in explicitly, these are `this` and `arguments`.
/*
The value of `this` depends on 1 of 4 types of "invocation patterns" used in javascript - 
1) method invocation pattern
2) function invocation pattern
3) constructor invocation pattern
4) apply invocation pattern
*/
The module pattern takes advantage of function scope and closure to create relationships
that are binding and private.
The general pattern of a module is a function that defines private variables and functions;
creates privileged functions which, through closure, will have access to the private
variables and functions; and that returns the privileged functions or stores them
in an accessible place.

/*
The values produced by typeof are 'number', 'string', 'boolean', 'undefined',
'function', and 'object'. If the operand is an array or null, then the result is
'object', which is wrong.

Numbers, strings, and booleans are object-like in that they have methods, but they are immutable. 
Objects in JavaScript are mutable keyed collections.
*/

//every object inherits properties from its prototype and so on until Object.prototype which is the 1st ancestor. To reflect and check only a current
//object without bubbling up to its ancestors, use
flight.hasOwnProperty('number');

//Currying allows us to produce a new function by combining a function and an argument:
var add1 = add.curry(1);
document.writeln(add1(6)); // 7

/*
At their most basic, promises are a bit like event listeners except:

1) A promise can only succeed or fail once. It cannot succeed or fail twice, neither can it switch from success to failure or vice versa.

2) If a promise has succeeded or failed and you later add a success/failure callback, the correct callback will be called, even though the event took place earlier.
This is extremely useful for async success/failure, because you're less interested in the exact time something became available, and more interested in reacting to the outcome.

fulfilled - The action relating to the promise succeeded
rejected - The action relating to the promise failed
pending - Hasn't fulfilled or rejected yet
settled - Has fulfilled or rejected
*/

//**********************************************************************************************************************************
//javascript as a language & js as a runtime, webAssembly & Rust
/*
WebAssembly (wasm) is a runtime. Not  a language you write by hand. Analogous to JVM byte code or x86 assembly.
Does not have a GC which js requires.

Rust is a modern systems programming language. Fast, safe (no mem corruption, no data races), 
productive. 

Apps - replacement for C , like to run on a microcontroller.
Uses LLVM compiler (which has a wasm backend) under-the-hood .
Used in Apple's stack, JVM compiler from Azul.
Rust has no GC, so no pauses.

Rust can run on big servers or tiny microcontrollers or a browser.
Rust doesnt have classes it has structs. Vec is a growable Array. 
Rust cleans up files. 

Rust has a small runtime (like C) which is in KBs, not MBs. 

Viable now- 
  1) sharing complex logic between server and browser
  2) working with binary data like JPEG or protobuf (painful in JS as there is no `byte` datatype, great in Rust, unsafe in C)
  3) perf-sensitive processing

In future - 
  1) SIMD
  2) Threads
  3) Entire webapps
*/

//**********************************************************************************************************************************
var a = 4;
{ 
  var a = 6;
}
//blocks dont have variable scope in javascript. This is unintuitive compared to classical languages like C++ and java, leading to a large class of errors
//But Javascript does have function scope. Variables declared and defined within a function are local to the function.
//Every object has its own namespace. Recommendation: best to declare variables at the top of each function than within a block to limit scope tightly.

//JavaScript does not have a linker. All compilation units are loaded into a common global object. In browsers, the global object is called `window`

/*
CSS selectors - 


css:
class name: $(".chatter-avatar")
id: $("#userThumbnailPhoto")
title: $("span[title='Test User']")


xpath:
$x(“//span[@id=’userThumbnailPhoto’]”)

http://jsbin.com/kuyun/5/edit?html,js,output
test html markup, css and js side by side for application security

TODO - https://free.codebashing.com/courses/php/lessons/sql_injection
application security vulnerabilities code walk through

solution: use `Elements` framework

TODO - https://xss-game.appspot.com
*/

var inputSelect = component.find("inputSelect");
inputSelect && inputSelect.isValid() && inputSelect.get(blablabla)
//Do these checks for other usecases too where you do .find().get()
//Reason is there are many situations when the component might be missing 
//(user gets logged out, tab needs to refresh , component loading failed etc)... better to silently fail in those cases


/*
If you create an aura component in javascript side, you must destroy the component too... otherwise the component will leak
Better to see if there is a way to put this component in the .cmp file and just add errors in helper by directly accessing the component
*/
//**********************************************************************************************************************************

/*

outerFunc() {
  innerFunc() {

  }.bind() //this makes sure thisInner == thisOuter , ie this referenced in innerFunc should actually refer to the outerFunc. In closures, its mandatory to use bind when you reference `this` in innerFunc
}

*/

example of promise in sfdc code - 
https://codesearch.data.sfdc.net/source/xref/app_main_core/app/main/core/ui-force-components/components/force/relatedListHover/relatedListHoverHelper.js#17

