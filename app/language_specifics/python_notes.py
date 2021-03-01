# adding a new egg  to python library -

# from within python shell -
import sys
sys.path.append("library1.egg")
# import foo

# from bash shell-
# export $PYTHONPATH
# ---------------
# testing reviewBoard python client -
# python python/lib/rbtools.py "cadmium", "1", "../output_data/rbdiffs/cadmium1.diff"

# python python/lib/rbtools.py "cadmium", "1", "/Users/ssatish/Projects/Ventana/output_data/rbdiffs/cadmium1.diff"
"""
rbclient_egg_path = os.path.join(os.path.dirname(
    "/Users/ssatish/Projects/Ventana/revenge/python/lib/rbtools.py"),
    "..", "..", "vendor", "python-2.7", "RBTools-0.6.3-py2.7.egg")
"""
# in ruby, test with rake task or like this -
# RAILS_ENV=dev_mock script/console
# > Release.generate_review_request "cadmium", "1",
# "/Users/ssatish/Projects/Ventana/output_data/rbdiffs/cadmium1.diff"

# testing on smash2 -
# >  Release.generate_review_request "cadmium", "1",
# "/home/revenge/ci/ci_release/output_data/rbdiffs/cadmium1.diff"
# ------
# rbtools python client API -
#rbtools.api.errors.AuthorizationError: You are not logged in (HTTP 401, API Error 103)

# review board docs -
# https://reviews.reviewboard.org/r/3843/diff/1#index_header

# programatically, can use the login method as well. Find out how!

# HTTP POST api/json/accounts/login/
# ------------
# draft = draft.update(target_people=TARGET_PEOPLE,target_groups=TARGET_GROUPS)
# rbtools.api.errors.BadRequestError: One or more fields had errors (HTTP 400, API Error 105)

"""
pip install pylint
pylint match/run/provider_cluster.py
"""
# -----------

# rbtools.api.errors.BadRequestError: One or more fields had errors (HTTP 400, API Error 105)

#    target_people: ['ssatish']

# ------------------
# create interface in python as an abstract base class -
# https://docs.python.org/2/library/abc.html

# http://stackoverflow.com/questions/372042/difference-between-abstract-class-and-interface-in-python
# NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))


# this is an example of using abstract methods in python below using module abc (abstract base class)-

import abc
class Shape(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def method_to_implement(self, input):
        """Method documentation"""
        return

# some abstract methods in an abstract class can also have an implementation; not all need to be empty;
# another example -
class Effable(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError('users must define __str__ to use this base class')

# you can use issubclass() or isinstance() to check an object against the abstract class

# more examples and registering an implementation  of an abstract class at -
# https://pymotw.com/2/abc/
# ----------------------
import abc
 
class BasePizza(object):
    __metaclass__  = abc.ABCMeta
 
    default_ingredients = ['cheese']
 
    @classmethod
    @abc.abstractmethod
    def get_ingredients(cls):
         """Returns the ingredient list."""
         return cls.default_ingredients
 
class DietPizza(BasePizza):
    def get_ingredients(self):
        return ['egg'] + super(DietPizza, self).get_ingredients()

#abstractmethod can return default values in partial implementation and still force children to
# override and implement it

# -----------------------------
#install anaconda 3.4.1 for mac OS X, downloaded from continuum analytics website (latest as of
# May 2017); installs python 3.6 along with it

# conda create --prefix env_conda_pyspark3p6 python=3.6
#creates a conda environment with certain versions of library packages
"""
conda env update -f provider_matching/wartime/facility_clustering/environment.yml

# this is how a sample env.yml looks like - 
name: matcherize
dependencies:
- python=3.5
- anaconda=4.2.0
- psycopg2=2.6.2
- seaborn=0.7.1
- pip:
  - ggplot==0.11.5
  - plotly==1.12.12
  - qgrid==0.3.2

# after conda installs all these dependencies, and creates the virtual environment named matcherize
 for you, you can activate it
source activate matcherize
source deactivate matcherize
"""
#------------------------------------
"""
pip3 install --upgrade pip
pip3 install jupyter

jupyter --version  # 4.3.0 gives Error executing command 'notebook' on python 3.4;
# Jupyter notebook only works with python 2.7 and 3.4+
pip3 install --upgrade --force-reinstall --no-cache-dir jupyter

# to deactivate a virtual env using anaconda
source deactivate

jupyter notebook
"""
# --------------------
# this is an outdated method that didn't work in May 2017 for intern. Anaconda is more up-to-date
# and easier to use
# install python2
# first install pip
"""
pip install --user virtualenv

# have this in your virtualenv 
/usr/local/bin/virtualenvwrapper.sh

# add these to your ~/.bash_profile
export WORKON_HOME=~/.virtualenvs
export PATH=/usr/local/bin:$PATH
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
source /usr/local/bin/virtualenvwrapper.sh

# virtual environment commands - 
mkvirtualenv duplo
workon duplo
deactivate - to exit virtualenv
"""
# ----------
# to reload classes, modules, functions in ipython (it has auto complete, so always use daconsole
# instead of plain python shell)


"""autoreload"""

# to view doc strings in ipython
"""%pdoc <function_name>"""

# ******ipython notes*****
# block comments in ipython -

"""
%cpaste
Pasting code; enter '--' alone on the line to stop or use Ctrl-D.
"""
# --------
# reload with code changes -
"""reload"""

# -----

# help within ipython
#------
# The reload command does a 'deep' reload of a module: changes made to the
#   module since you imported will actually be available without having to exit.
# --------
import ipdb; ipdb.set_trace()

"""
help (h) 
where (prints stack trace)
c (continue)
n (next)
"""
# ---------
#unit integration tests debugging with python debugger step thru breakpoints
#all you need to do is call py.test with the --pdb flag and it pops you into the debugger at the point where an exception is raised
"""python -m ipdb module.py"""

# Pro Python Best Practices: Debugging, Testing and Maintenance
# By Kristian Rother
#to set a conditional breakpoint, you can have a .pdbrc file with regular commands along with
# breakpoint commands as follows
# source: Pro Python Best Practices: Debugging, Testing and Maintenance, By Kristian Rother
# contents of .pdbrc file
from pprint import pprint
"""
ll
print(dir())
b maze_run.handle_key
b moves:27, level[newy][newx] == '#'  # this is a conditional breakpoint on a condition
"""
# ----------

"""python -m ipdb pipeline.py -args"""

"""
%debug 
# to enter post mortem debug mode ; doesnt work if u catch and dont re-raise exceptions;
then exception wont buble up to ipython;
"""
# -----
# command cmd history -

"""
 _i: stores previous input.
  _ii: next previous.
  _iii: next-next previous.
  _ih : a list of all input _ih[n] is the input from line n.
"""
# ------
# %pastebin 3 18-20 ~1/1-5
# This will take line 3 and lines 18 to 20 from the current session, and lines 1-5 from the previous session.
# ----------
# daconsole -version says ipython 4.0.0 and python 2.7.10 is being used for duplo
#
# ipython under the hood uses a message passing interface using json.
# But this implementation can change in future, since JSON has non-trivial performance issues due to excessive copying.
# The proposal is to move to a pickle-based raw message format.
#
# If IPython doesn’t know what to do with an object, it will pickle it.
# There is a short list of objects that are not pickled: buffers, str/bytes objects, and numpy arrays.
#  These are handled specially by IPython in order to prevent the copying of data. Sending bytes or numpy arrays will result in exactly zero in-memory copies of your data (unless the data is very small).
#
# Just about anything in Python is pickleable. The one notable exception is objects (generally functions) with closures.
# Closures can be a complicated topic, but the basic principle is that functions that refer to variables in their parent scope have closures.
#
# A closure is a function object that remembers values in enclosing scopes regardless of whether those scopes are still present in memory.
# eg - a function that returns another function. A class is data with operations attached. A closure is operations with data attached.
#
# # in python 3.5,  if add_to_5 is a closure as defined below, to see the contents introspectively,
# def generate_adder_func(n):
#     def adder(x):
#         return n + x
#
#     return adder
# add_to_5 = generate_adder_func(5)
#
# add_to_5.__closure__[0].cell_contents
# # every function object has __closure__ attribute. If there is no data for the closure, __closure__ will be None.
# -----------
# synchronous = blocking function calls in ipython.paraller or ipyparallel
# asynchronous = non-blocking function calls by returning an AsyncResult object immediately without freezing your ipython terminal session
#
# *****end ipython notes******
# -----------
# #getters in python can be identified with the decorator below
# @property
# def shares(self):
# 	return self._shares
#
# #setters can be identified with the decorator
# @shares.setter
# def shares(self, value):
# 	if not isinstance(value, int):
# 		raise TypeError('expected int')
# 	if value < 0:
# 		raise ValueError('Must be >=0')
# 	self._shares = value
#
# #accessing an object by index
# #python construct/keywords => underlying magic methods called
# obj[i]                     => __getitem__
# for obj in                 => __iter__
# obj.                       => __getattr__
# if..in                     => __contains__
# len()                      => __len__
# int()                      => __int__
# if condn / bool()          => __nonzero__
# +                          => __add__
# |                          => __and__
# wrap any method with context manager => @contextlib.contextmanager decorator (can have custom __enter__ and __exit__ )
# #---
# #now what if you wanted to have validation for each field in a class input , eg customized handling of a specific attribute
# #above properties (getter/setter) are implemented via descriptors
# class Descriptor:
# 	def __init__(self, name=None):
# 		self.name = name
#
# 	def __get__(self, instance, cls):
# 		if instance is None:
# 			return self
# 		else:
# 			return instance.__dict__[self.name]
#
# 	def __set__(self, instance, value):
# 		instance.__dict__[self.name] = value
#
# 	def __delete__(self, instance):
# 		del instance.__dict__[self.name] or raise AttributeError("Can't delete")
# #Type Checking
# class Typed(Descriptor):
# 	ty = object
# 	def __set__(self, instance, value):
# 		if not isinstance(value, self.ty):
# 			raise TypeError('Expected %s')
# 		super().__set__(instance, value)
#
# class Integer(Typed):
# 	ty = int
# class Float(Typed):
# 	ty = float
# class String(Typed):
# 	ty = str
#
# #usage_basic
# class Spam:
# 	x = Descriptor()
# s = Spam()
#
# s.x	         # x.__get__(s, Spam)
# s.x = value	 # x.__set__(s, value)
# del s.x      # x.__delete__(s)
#
#
# #usage_advanced
# class Stock(Structure):
# 	_fields = ['name', 'shares', 'price']
# 	name = String('name')
# 	shares  = Integer('shares')
# 	price = Float('price')
# -------------
# range() returns  a list while range returns an object
#
# The advantage of the range type is that an range object will always take the same amount of memory, no matter the size of the range it represents. There are no consistent performance advantages.
# range objects (immutable sequence) have very little behavior: they only support indexing, iteration, and the len() function.
# -------------------
# string formatting for octal and hexadecimal -
# print "Octal = %#o Hexadecimal = %#x" % (number, number)
# ----------
# dir() on python shell tells you what modules are imported and in scope -
# dir(test_data_interface.TestDataInterface._get_address_query)
#
# returns ['__call__',
#  '__class__',
#  '__closure__',
#  '__code__',
#  '__defaults__',
#  '__delattr__',
#  '__dict__',
#  '__doc__',
#  '__format__',
#  '__get__',
#  '__getattribute__',
#  '__globals__',
#  '__hash__',
#  '__init__',
#  '__module__',
#  '__name__',
#  '__new__',
#  '__reduce__',
#  '__reduce_ex__',
#  '__repr__',
#  '__setattr__',
#  '__sizeof__',
#  '__str__',
#  '__subclasshook__',
#  'func_closure',
#  'func_code',
#  'func_defaults',
#  'func_dict',
#  'func_doc',
#  'func_globals',
#  'func_name']
# ------------
# to see all the builtin exceptions -
#
# >>> import exceptions
# >>> help(exceptions)
# or
# >>> help('exceptions')
# ---------
# import glob -
#  glob and walk to find all the files in a directory
# structure that match the pattern, just like the 'find' command in unix.
# ------------------
# import subprocess
#
# piper.py - has an example of wrapping unix cmds with subprocess module in python and executing them.
# -------
# make  a persistent dictionary by shelving it -
#
# import shelve
#
#
# dictionary and list are mutable data types in python 2.7
# ----------------
# # Generators are data producers
# generators in python are iterables that dont hold all values in memory, they generate 1 value, then forget about it, then generate the next value in a sequence, etc ..
#
# mygenerator = (x*x for x in range(3))
# >>> for i in mygenerator:
# ...    print(i)
#
# the difference between generator and list is the () instead of []
#
#
# in generators, you can only read a value ONCE, ie, its a single pass iterator
#
# Yield is a keyword that is used like return, except the function will return a generator.
#
# To master yield, you must understand that when you call the function, the code you have written in the function body does not run. The function only returns the generator object, then, your code will be run each time the for uses the generator.
#
# Tip: always try to Use the iterator-methods on dictionaries
# dictionaries come with these methods from ptyonn 2.2+
# iterkeys(), itervalues() and iteritems().
# They yield the same data as keys(), values() and items() do, but instead of returning lists they return iterators, which saves memory and time when using large dictionaries
#
# using for x in dict
# will use iterators automatically in both Python 2 and Python 3.
#
# # eg recipe round-robin counter using generators
# def round_robin():
#     while True:
#         yield from [1,2,3,4]
#
# a = round_robin()
# next(a)  # 1
# next(a)  # 2
#
# #-----------------------------------
# # Coroutines are data consumers
#
# def coroutine():
#     while True:
#         val = (yield)
#         print(val)
#
# a = coroutine()
# next(a)
# a.send(1)  # 1
# a.close()
#
# b = coroutine()
# b.send(None)
# b.send(1)
#
# # all coroutines must be "primed" by first calling next() or send(None). This advances execution to the location of the first `yield` expression.
# # For the first "yield", it is ready to receive the values
# # Call "close" to shut down the coroutine.
# ---------------------------------------
# block comment toggle in pycharm IDE - <cmd> /
#
# pycharm replace all tabs with spaces -
# code -> reformat code
# given that you've already setup 4-spaces instead of tabs, this automatically takes care of it for you
# --------
# pretty print complex nested objects like dictionaries -
#
# pip install pretty
# from pretty import pprint
# ----------------
#
# iterables implement the __iter__() method
# and
# iterators implement the __next__() in python 3.0 or next() in python 2.0 method
#
# iterables are any objects you can get an iterator from.
# iterator is any object that lets you iterate on iterables
# ----------------
# #nose, tox, pytest - unit test frameworks;
#
# #tox runs tests against 2 different DBs;
# #cfg for test is tox.ini
#
# #if you get - DataSourceProcess.ValidationError: There is no release_label for the current period in the provider_master_prod_v5_10 database. Its due to outdated CDW release_label in 1 of its state-maintaining tables. its updated in prov_dir_template and to get latest tables from there, run -
#
# tox -e integration-cleanup,integration-setup
# prov_dir_automaton_integration_test_e621ed
#
# #anyway if you do ever want to set an env variable in tox, use setenv https://testrun.org/tox/latest/config.html#confval-setenv=MULTI-LINE-LIST
# #if you want tox to get an existing environment variable, use passenv https://testrun.org/tox/latest/config.html#confval-passenv=SPACE-SEPARATED-GLOBNAMES
#
# every time there is a push on duplo-greenplumize,  CI tests run by creating a database called prov_dir_automaton_<commit #>
# and then that DB gets dropped. all schemas are cloned from prov_dir_template. for raw exception handling you need to create 4 tables within the raw schema
# ----------------------
# pip install dedupe-variable-address
# pip install dedupe-variable-name
#
# pip install 'dataenv==0.10.2'
# pip install -U 'scikit-learn==0.18.1'  # upgrades sklearn from 0.17 to 0.18.1
# -----------------------------------
# from nltk.tag.stanford import StanfordNERTagger
# ---------------
# to start local pip server -
# devpi-server --start
#
# pip install -i http://localhost:3141/root/pypi/ simplejson
#
# -------
# Uploading Python Packages to Devpi (pip )
# https://confluence.castlighthealth.com/display/DEV/Uploading+Python+Packages+to+Devpi
#
# devpi use http://den-gp2-standby01.ch.int:3141/ssaneinejad/clh
# devpi login ssaneinejad --password=
# devpi upload
#
# to remove a particular version of library from devpi server,
#
# devpi index -l
# #ssaneinejad/clh this is the current index
#
# devpi list
# #lists the packages that exist on the devpi server
#
#
# devpi remove -y provider_matching==1.0.0
# #DELETE http://den-gp2-standby01.ch.int:3141/ssaneinejad/clh/provider-matching/1.0.0
# #403 Forbidden: cannot delete version on non-volatile index
# #instead use below
# devpi-cleaner http://den-gp2-standby01.ch.int:3141 ssaneinejad/clh 'provider_matching==1.0.3' --force
# #deletes the devpi packages from devpi server
#
# devpi refresh provider_matching==1.0.0
# #this didnt really refresh it and put the config/ folder although it has __init__.py within it
#
# #to see which files are missing in virtual env package, the below cmd showed 285 files in git version vontrol but only 165 files made it to pkg
# check-manifest -u -v
# #most notably, config/logging.yaml was missing. it can be added to pkg by including the line in manifest.in  which check-manifest automatically does
#
# #if you see the latest version of package in devpi not being pulled during pip install, thats because pip locally caches library versions under
# #/home/ssatish/.cache/
# # you have to force pip to not use the cache and pull from latest devpi server. check how to do that
# pip install 'provider_matching==1.0.3' --no-cache-dir
# # the above cmd runs the below cmd under the hood
# #Installing collected packages: provider-matching
# #  Running setup.py install for provider-matching
# #this setup.py is not set up to install yaml/yml files.
# #python ./setup.py bdist  (installed yaml files after modification to setup.py; this is what pip install also does under the hood, ie bdist)
#
# pip install provider_matching --upgrade
# ---------
# gensim serialized format to numpy and csipy sparse matrix formats -
#
# corpus = gensim.matutils.Dense2Corpus(numpy_matrix)
# numpy_matrix = gensim.matutils.corpus2dense(corpus, num_terms=number_of_corpus_features)
#
# corpus = gensim.matutils.Sparse2Corpus(scipy_sparse_matrix)
# scipy_csc_matrix = gensim.matutils.corpus2csc(corpus)
# -------------
# how to see what data structure is an object in python  (list, string, nested dict, etc)?
#
# type(item) method.
# but above method is not preferred, instead below is preferred pythonic way in recent times
# if isinstance(item, int):
#        del mylist[item]
# -------------
#
# to check (introspect) if a function exists in an object, (like reflection on methodExists? in java)
# use hasattr() method;
# -----
# string concatenation in python -
#  str.join() method which assures consistent linear concatenation performance across versions and implementations compared to the s+j or '+' operator
# -------
# hashable object in python -  Hashable objects which compare equal must have the same hash value. hashable object is 1 which implements the __hash__() method
# and 1 of __eq__() or __cmp__() methods; Hashability makes an object usable as a dictionary key and a set member, because these data structures use the hash value internally. All of Python’s immutable built-in objects are hashable, while no mutable containers (such as lists or dictionaries) are. Objects which are instances of user-defined classes are hashable by default; they all compare unequal (except with themselves), and their hash value is their id().
#
# --------
# set data type in python - its an unordered collection of distinct hashable objects; but a set is mutable;
# Since it is mutable, it has no hash value and cannot be used as either a dictionary key or as an element of another set.
#
# The frozenset type is immutable and hashable — its contents cannot be altered after it is created; it can therefore be used as a dictionary key or as an element of another set.
#
# Set() constructor as well as declaring in braces creates sets like {'jack', 'sjoerd'}
# -------------------
# class.__mro__
# This attribute is a tuple of classes that are considered when looking for base classes to determine  method resolution order.
#
# class.mro()
# This method can be overridden by a metaclass to customize the method resolution order for its instances. It is called at class instantiation, and its result is stored in __mro__.
#
# class.__subclasses__()
# Each new-style class keeps a list of weak references to its immediate subclasses. This method returns a list of all those references still alive.
# -----
# double ended queue implementation in python 2.7 -
# # collections.deque is an alternative to Queue module.
# # It providers unbounded queue with fast atomic append() and popleft() that do not require locking
# Deques support thread-safe, memory efficient appends and pops from either side of the deque with approximately the same O(1) performance in either direction.
#
# Though list objects support similar operations, they are optimized for fast fixed-length operations and incur O(n) memory movement costs for pop(0) and insert(0, v) operations which change both the size and position of the underlying data representation.
#
#  defaultdict - this is another powerful data structure in python which can be used in many ways to aggregate key-value pairs like in map-reduce style ; refer examples in documentation -
# https://docs.python.org/2/library/collections.html#defaultdict-examples
#
# ----
# #other python standard library implementations of priority queue -
# # [A]
# import heapq
# heapq.heappush(heap, item)
# item = heapq.heappop(heap) # raises IndexError for pop-from-empty
# # for peek, use heap[0]
# item = heapq.heapreplace(heap, item)  # pops smallest and returns it as item, also adds new item
# # onto heap
#
# heapq.nlargest(n, iterable[, key])
# heapq.nsmallest(n, iterable[, key])
#
# # application 1
# def heapsort(iterable):
#     h = []
#     for v in iterable:
#         heappush(h, v)
#     return [heappop(h) for i in range(len(h))]
#
# # heap elements can be tuples as well as shown blow
# # application 2
# h = []
# heappush(h, (5, 'write code'))
# heappush(h, (7, 'release product'))
# heappush(h, (1, 'write spec'))
# heappush(h, (3, 'create tests'))
# heappop(h) # (1, 'write spec')
#
# # application 3 : Design of jira priority management of tasks. For tasks of same priority, use FIFO order.
# pq = []
# entry_finder = {} # this is for searching jira by key
# counter = itertools.count()
# REMOVED = 'removed'
# def add_task(task, priority=0):
#     """
#     add a new task or update the priority of an existing task
#     """
#     if task in entry_finder:
#         remove_task(task)
#     count = next(counter)
#     entry = [priority, count, task]
#     pq.heappush(entry)
#     entry_finder[task] = entry
#
# def remove_task(task):
#     """
#     Mark an existing task as REMOVED. Raises KeyError if not found
#     """
#     entry = entry_finder.pop(task)
#     entry[-1] = REMOVED
#
# def pop_task():
#     """
#     Remove and return the lowest priority task.
#     Raises KeyError if empty
#     """
#     while pq:
#         priority, count, task = heappop(pq)
#         if task is not REMOVED:
#             del entry_finder[task] # Deletion of a task removes the binding of that task from the local or global namespace
#             return task
#     raise KeyError('pop from an empty priority queue')
# #--
# # [B]
# import Queue # this module has been renamed to queue in python 3
# # This implements multi-producer, multi-consumer queues (thread-safe).
# # has 3 classes LifoQueue (like stack), Queue, PriorityQueue (uses heapq module under-the-hood)
# # public methods by all 3 objects -
# Queue.qsize()
# Queue.empty()
# Queue.full()
#
# Queue.put(item[block[, timeout]]) # if full, blocks until space is made , for max timeout time. If timeout, raises Queue.Full exception
# Queue.put_nowait() # non-blocking, equivalent to put(item, False)
# Queue.get([block[, timeout]])
# Queue.get_nowait()
#
# Queue.task_done() # indicate that a formerly enqueued task is complete. For every get(), task_done() tells the q that processing on that item is done; useful for daemon consumer threads
# Queue.join() # blocks until all items in the Q have been processed
#
# # Example of how to wait for enqueued tasks to be completed:
# def worker():
#     while True: # note that if you use "for i in q:" instead, you wil get TypeError("Iteration over non-sequence")
#         item = q.get()
#         item.process()
#         q.task_done()
#
# q = Queue()
#
# for i in range(num_worker_threads):
#     t = Thread(target=worker)
#     t.daemon = True
#     t.start()
#
# for item in source():
#     q.put(item)
#
# q.join() # block until all tasks are done
# ----------------
# # ideal data structure to read records from database (or flat csv) is namedtuple -
# # name,age,title,department,paygrade
# # suhas,29,"Senior Software Engineer",revenge,2
#
# EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')
#
# # sample usage - name of the tuple is the first argument, followed by list of fields
# Point = namedtuple('Point', ['x', 'y'])
#
# import csv
# for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
#     print emp.name, emp.title
#
# import sqlite3
# conn = sqlite3.connect('/companydata')
# cursor = conn.cursor()
# cursor.execute('SELECT name, age, title, department, paygrade FROM employees')
# for emp in map(EmployeeRecord._make, cursor.fetchall()):
#     print emp.name, emp.title
# --------------
# Stackless Python - a python implementation that does not use the C stack
# pros: its not limited by the size of the C functional call stack, but only by the available heap memory
#      It also lets you run 100s to 1000s of tiny tasks called tasklets in a single main thread. they can run completely decoupled and communicate via channels.
# Channels take all the responsibility to control suspension and resuming of tasklets in an easy-to-manage way.
# ------------
#
# http://www.dabeaz.com/python/GIL.pdf
#
# Current primary reference implementation of python -Cpython has the GIL problem. For single-threaded (non-concurrent) applications, the existing reference-counting of objects mechanism is very fast. It means that almost any reference to an object is a modification (atleast to the refcount). Many concurrent Garbage collection algorithms assume that modifications are rare.
#
# GIL ensures that each thread gets exclusive access to the python interpreter internals when its running. Threads hold the GIL mutex while running. Hoever, they release it when blocking for I/O. When a thread is waiting on I/O, other "ready" threads get their chance to run.
#
# So CPU-bound threads that never are blocked on IO, the interpreter periodically performs a "check", every 100 interpreter ticks. Ticks are uninterruptible (ctrl-C signal cannot kill it), and NOT time-based. Long operations can block everything . eg - nums in range(100000000); -1 in nums ; takes 6.6 seconds to iterate over whole array and then return result.
#
# The above implies that threaded operations in python cannot be killed with keyboard interrupt. You have to use kill -9 in a separate window.
# Signal handlers can only run in the main thread. The interpreter quickly acquires/releases the GIL after every tick until it gets scheduled.
# Python does NOT have a thread scheduler.
# There is no notion of thread priorities, preemption, round-robin scheduling, etc
# All thread scheduling is left to the host operating system .
# This means the python interpreter has no control over scheduling so it just attempts to thread switch as fast as possible with the hope that main thread will run (having signal handling code)
#
# CPU bound thread - low priority
# IO bound thread - high priority
# If a signal is sent to a thread with low priority and CPUs are busy with some higher priority tasks, it wont run until some later point.
# ----------
# data parallelism with single program (function) can be achieved to harness all cores of a multi-core machine by using  -
# from multiprocessing import Pool
#
# 1)
# in the multiprocessing, inter-process communication can take place via 2 mechanisms - queue or pipe. a pipe returns 2 connection objects connected by a pipe. A pipe allows only 1 single producer and a single consumer, but a queue allows multiple producers and consumers.
#
# 2)
# when doing concurrent programming, its best to avoid shared state. but if you do want to use shared state, there are 2 ways -
#   a) shared memory  b) server process manager
#
# A manager object returned by Manager() controls a server process which hols python objects and allows  other processes to manipulate them using proxies;
#
# Server process managers are more flexible than using shared memory objects because they can be made to support arbitrary object types (data structures). Compared to this, shared memory supports only Array type and Value type.
#
# Also, a single manager can be shared by processes on different computers over a network. They are, however, slower than using shared memory.
#
# Some programing guidelines using multiprocessing:
# 1) As far as possible one should try to avoid shifting large amounts of data between processes.
# Shahin saw this when the parent process took forever to transfer portions of 7 GB table on-disk into the heap memory of child-processes.
# With top, it could only load data into 2-3 child processes and the other 7 child processes spawned in the pool were still waiting for their
# heaps to be loaded.
#
# 2)
# ------------------
#
# sys.setcheckinterval() changs the check interval setting. The check interval is a global counter that is completely independent of thread scheduling.
# ---------------
# this is a closure in python -
# def f(a):
#     def inner():
#         # inner will have a closure
#         return a
#     return inner
#
# -----------
# #The compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)
# #built-in can be used to speed up repeated invocations of the same code with exec or eval by compiling the source into a
# # code object beforehand. The mode parameter controls the kind of code fragment the compile function accepts and the kind of
# #bytecode it produces. The choices are 'eval', 'exec' and 'single'
# =============================================================================================
# python 3 metaprograming - decorators, DRY - dont-repeat-yourself principles : David Beazley talk pyCon 2013
#
# do not use lists, dictionaries and other mutable data structures as default arguments in a function as they are set only
# once and can lead to subtle bugs.
#
# below method signature only in python3.
# def recv(maxsize, *, block=True)
# Named arguments after '*' can only be passed by keyword.
# recv(8192, block=False)  #ok
# recv(8192,False) #error
# --------
# different  method types -
#
# class Spam:
#   def imethod(self):
#     pass
#
# 	@classmethod
# 	def cmethod(cls):
# 		pass
#
# 	@staticmethod
# 	def smethod():
# 		pass
#
# Usage:
# s = Spam()
# s.imethod()
#
# Spam.cmethod()
#
# Spam.smethod()
# ---------
# when to use python module methods vs classmethod vs staticmethod in python -
#
# #A static method in Java does not translate to a Python classmethod. Oh sure, it results in more or less the same effect, but the goal of a classmethod is actually to do something that's usually not even possible in Java (like inheriting a non-default constructor). The idiomatic translation of a Java static method is usually a module-level function, not a classmethod or staticmethod. (And static final fields should translate to module-level constants.)
#
# #This isn't much of a performance issue, but a Python programmer who has to work with Java-idiom code like this will be rather irritated by typing Foo.Foo.someMethod when it should just be Foo.someFunction. But do note that calling a classmethod involves an additional memory allocation that calling a staticmethod or function does not.
#
# #Oh, and all those Foo.Bar.Baz attribute chains don't come for free, either. In Java, those dotted names are looked up by the compiler, so at runtime it really doesn't matter how many of them you have. In Python, the lookups occur at runtime, so each dot counts. (Remember that in Python, "Flat is better than nested", although it's more related to "Readability counts" and "Simple is better than complex," than to being about performance.)
#
# http://stackoverflow.com/questions/11788195/module-function-vs-staticmethod-vs-classmethod-vs-no-decorators-which-idiom-is
#
# #The most straightforward way to think about it is to think in terms of what type of object the method needs in order to do its work. If your method needs access to an instance, make it a regular method. If it needs access to the class, make it a classmethod. If it doesn't need access to the class or the instance, make it a function. There is rarely a need to make something a staticmethod, but if you find you want a function to be "grouped" with a class (e.g., so it can be overridden) even though it doesn't need access to the class, I guess you could make it a staticmethod.
#
# #I would add that putting functions at the module level doesn't "pollute" the namespace. If the functions are meant to be used, they're not polluting the namespace, they're using it just as it should be used. Functions are legitimate objects in a module, just like classes or anything else. There's no reason to hide a function in a class if it doesn't have any reason to be there.
#
# -----
# instance variables of a class and instance methods are stored internally as a dict.
#
# When you construct an object Python calls its __new__ method to create the object then calls __init__ on the object that is returned. When you create the object from inside __new__ by calling Triangle() that will result in further calls to __new__ and __init__.
#
# eg- objects are layered on dictionaries
#
# class Spam:
# 	def __init__(self,x,y):
# 		self.x = x
# 		self.y = y
#
# 	def foo(self):
# 		pass
#
# s = Spam(2,3)
#
# s.__dict__
# {'y' = 3, 'x' = 2}
#
# Spam.__dict__['foo']
# --------------
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
# #above cmd is include in top-level python file (entry-point to code) and gives  path to the logging.conf settings file
#
# #decorator is a func which takes a function as input
# 100
# from functools import wraps
# import logging
#
# def debug(func):
# 	if 'DEBUG' not in os.environ:
# 		return func
# 	log = logging.getLogger(func.__module__)
# 	msg = func.__qualname__
# 	@wraps(func)  #this prints meta function doc string from the decorated function
# 	def wrapper(*args, **kwargs):
# 		log.debug(msg)
# 		print(func.__name__)
# 		return func(*args,**kwargs)
# 	return wrapper
#
#
# from debugly import debug
# @debug
# def *
#
# #advantage: debugging code is isolated to a single location;
# #key idea - can change decorator independently of core logic in module methods
#
# #CAVEAT - a decorated function's __name__attribute changes
# def my_decorator(func_obj):
#     def wrapped(*args, **kwargs):
#         return_obj = func_obj(*args, **kwargs)
#
# @my_decorator
# def my_func(name)
#     pass
# my_fun.__name__ # returns 'wrapped'. To preserve the original function object's metadata like name, doc string, annotations and calling signatures, use the decorator "@wraps" in the wrapped() function above.
# #-----------
#
# #decorators with args
#
# #outer function (decorate) defines variables for use in regular decorator
# def debug(prefix=''):
# 	def decorate(func):
# 		msg = prefix + func.__qualname__
#
#         @wraps(func)
# 	def wrapper(*args, **kwargs)
# 		print(msg)
#
# #usage
# @debug(prefix='***')
#
# # eg using factorial using memoization with decorators
# def memoize(f):
#     memo = {}
#     def helper(x):
#         if x not in memo:
#             memo[x] = f(x)
#         return memo[x]
#     return helper
#
# @memoize
# def factorial(n):
#     if n == 0 or n == 1:
#         return 1
#     else:
#         return n * factorial(n-1)
# #-------
# #classmethod
#
# def debugmethod(cls):
# 	#cls is a class
# 	#vars gives the class dictionary
# 	for key, val in vars(cls).items():
# 		if callable(val):
# 			setattr(cls, key, debug(val))
#
# #usage  - does not work with @classmethod and @staticmethod
# @debugmethods
# class Spam:
# 	def __init__(self):
# 		pass
#
# #----------------
# def debug_attr(cls):
# 	orig_getattribute = cls.__getattribute__
# 	#yanks off class atttribute look-up method
#
# 	def __getattribute__(self, name):
# 		print('Get:', name)
# 		return orig_getattribute(self, name)
#
# 	cls.__getattribute__ = __getattribute__
# 	return cls
# #-------------------
# #class is the type of instances created, ie classes are instances of types
# #class is a callable that creates instances
#
# s = Spam()
# type(s)
#
# returns <class '__main__.Spam'>
#
# #when a class is declared & defined , these are the things happenin under the hood in python 3.3+
# #step 1
# clsdict = type.__prepare__('Spam', (Base,))
# #this dict serves as local namespace for statements in the class body
#
# #step 2 : body of class is executed in returned dict
# exec(body, globals(), clsdict)   #built-in function globals() returns the global dict and locals() the local dict
# # eval('42') -> returns 42 (the value) ; use it for single expressions
# #exec('42') -> returns None; use it to execute dynamically created statements
# #exec accepts source code that contains statements, like def, for, while, import, or class, the assignment statement (a.k.a a = 42), or entire programs
# #both call compile() method under the hood, like compile(source, '<string>', 'exec')
#
# # In Python 2, the official syntax for the exec statement is actually `exec code in globals, locals` :
# #or alternate syntax exec(code, globals, locals)
#
#
# #step 3 : clsdict is populated
# clsdict
# {'__init__': <function __init__ at 0x4da10>,
#  'bar': <function bar at 0x4dd70>}
#
# #step 4 : class is constructed from its name, base classes and the dictionary
#
# Spam = type('Spam', (Base,), clsdict)
# #-------------
# #metaclasses like type class which makes classes itself, can be subclassed to modify default functionality;
#
# #metaclass get information about class definitions at the time of definition
# 	#can inspect this data
# 	#can modify this data
#
# #similar to a class decorator
# #metaclasses propagate down heirarchies, unlike decorators;
#  {decorators: functions
# 	class decorators: classes
# 	metaclasses: class heirarchies}
# #------------------
# #avoiding repeated-initialization of values using setters in constructors
#
# #structly.py
# class Structure:
# 	_fields = []
# 	def __init__(self, *args):
# 		for name, val in zip(self.__class__._fields, args):
# 			setattr(self, name, val)
#
# class Stock(Structure):
# 	_fields = ['name', 'shares', 'price']
#
# class Point(Structure):
# 	_fields = ['x', 'y']
#
# class Address(Structure):
# 	_fields = ['hostname', 'port']
# #note that in the above example, u can access class variables thru an instance;
# #disadvantage of above design -
# # 1) you lose keyword arguments
# #    like s = Stock(name='GOOG')  will threw error
# # 2) help(Stock) will only display __init__(self,*args) ; without giving out the constructor's details or argument signatures
#
# #----------------------
# import inspect
# from inspect import Parameter, Signature
# inspect.signature(Stock) #new in python 3.3 shows signature
#
# parms = [ Parameter(fname, Parameter.POSITOINAL_OR_KEYWORD) for fname in _fields]
# sig = Signature(parms)
#
# #Signature binding to *args and **kwargs
# def foo(*args, **kwargs):
# 	bound_args = sig.bind(*args, **kwargs)  # binds positional/keyword args to signature
# 	for name, val in bound_args.arguments.items():
# 		print(name, '=', val)  #.arguments is an OrderedDict of passed values
#
# def make_signature(names):
# 	return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)
#
# class Structure:
# 	__signature__ = make_signature([])
# 	def __init__(self, *args, **kwargs):
# 		bound = self.__signature__.bind(*args, **kwargs)
# 		for name, val in bound.arguments.items():
# 			setattr(self, name, val)
#
# #--------------
# #combining above ideas with decorators -
# def add_signature(*names):
# 	def decorate(cls):
# 		cls.__signature__ = make_signature(names)
# 		return cls
# 	return decorate
#
# @add_signature('x', 'y')
# class Point(Structure):
# 	pass
# #-------------------
# #same effect as above but with Metaclass instead of decorators -
# class StructMeta(type):
# 	def __new__(cls, name, bases, clsdict):
# 		clsobj = super().__new__(cls, name, bases, clsdict)
# 		sig = make_signature(clsobj._fields)
# 		setattr(clsobj, '__signature__', sig)
# 		return clsobj
#
#
# class Structure(metaclass = StructMeta):
# 	_fields = []
# 	def __init__(self, *args, **kwargs):
# 		bound = self.__signature__.bind(*args, **kwargs)
# 		for name, val in bound.arguments.items():
# 			setattr(self, name, val)
#
# #advice:
# # 1) use a class decorator if goal is to tweak classes that are unrelated
# # 2) use metaclass if you're trying to perform actions in combination with inheritance
# --------------
# #best way to declare list of lists in pythonic way
# four_lists = [[] for __ in range(4)]
#
# # list comprehension example - pythonic way
# ','.join([str(x) for x in foo])
#
# # order them in the same way they would be writen from left to right in for loop
# [int(x) for line in data for x in line.split()]
# # when not nesting the ordering is same as in for-loop. Note the difference with below.
#
# # 2D dimensional matrix initialization in pythonic way -
# x = [[0 for j in range(10)] for i in range(10)]
# # when writing nested lists for 2D array, its in the inside-out order of writing for-loop.
# # for i in range(N1):
# #   for j in range(N2):
# #       for k in range(N3):
# #is written as [[[0 for k in range(N3)] for j in range(N2)] for i in range(N1)]
#
# --------
# sorting - using the 'key=' is much faster o(n lg n) vs using the 'cmp=' which compares all pairs ie o(n^2 lg n)
#
# #bad and slow
# names.sort(cmp=compare)
#
# #good -  easier to use and faster to run
# #key function is only called once for every item
# names.sort(key=lambda x: x[1:], reverse=True)
#
# def keyfunction(item):
#   """Key for comparison that ignores the first letter"""
#   return item[1:]
# >>> names = ['Adam', 'Donald', 'John']
# >>> names.sort(key=keyfunction)
# ---
#
# # to sort with the longest names first and names of the same length sorted alphabetically
# # sort twice, with the LEAST important sorting FIRST.
#
# >>> names = ['Adam', 'Donald', 'John']
# >>> # Alphabetical sort
# >>> names.sort()
# >>> # Long names should go first
# >>> names.sort(key=lambda x: len(x), reverse=True)
#
# #reason above code works is because under the hood, python 2.4+ uses STABLE sort, which maintains the sort order of equal-valued keys
# ------------------
#
# best way to implement custom comparators which works in both python2 and python 3 is to use this
# mixin template -
#
# class ComparableMixin(object):
#     def _compare(self, other, method):
#         try:
#             return method(self._cmpkey(), other._cmpkey())
#         except (AttributeError, TypeError):
#             # _cmpkey not implemented, or return different type,
#             # so I can't compare with "other".
#             return NotImplemented
#
#     def __lt__(self, other):
#         return self._compare(other, lambda s, o: s < o)
#
#     def __le__(self, other):
#         return self._compare(other, lambda s, o: s <= o)
#
#     def __eq__(self, other):
#         return self._compare(other, lambda s, o: s == o)
#
#     def __ge__(self, other):
#         return self._compare(other, lambda s, o: s >= o)
#
#     def __gt__(self, other):
#         return self._compare(other, lambda s, o: s > o)
#
#     def __ne__(self, other):
#         return self._compare(other, lambda s, o: s != o)
#
# >>> from mixin import ComparableMixin
#
# >>> class Orderable(ComparableMixin):
# ...
# ...     def __init__(self, firstname, lastname):
# ...         self.first = firstname
# ...         self.last = lastname
# ...
# ...     def _cmpkey(self):
# ...         return (self.last, self.first)
# ...
# ...     def __repr__(self):
# ...         return "%s %s" % (self.first, self.last)
# ...
# >>> sorted([Orderable('Donald', 'Duck'),
# ...         Orderable('Paul', 'Anka')])
# [Paul Anka, Donald Duck]
#
# sorted() - #this function returns a new sorted list, original list is unmodified (ie, not
# in-place sort)
# x = 'bug'
# sorted(x) -> returns ['b', 'g', 'u']
#
# list.sort() on the other hand, does an in-place sort
# ------------------------
# In Python 2, if you implement __eq__() you should also override __hash__(). This is because two
# objects that compare equal should also have the same hash-value. If the object is mutable, you
# should set __hash__ to None, to mark it as mutable. This will mean you can't use it as a key in
# dictionaries for example, and that's good, only immutable objects should be dictionary keys.
#
# In Python 3, __hash__ will be set to None automatically if you define __eq__(), and the object
# will become unhashable, so for Python 3 you don't need to override __hash__() unless it is an
# immutable object and you want to be able to use it as a key value.
#
# The value returned by __hash__() needs to be an integer, and two objects that compare equal
# should have the same hash value. It must stay the same over the whole lifetime of the object,
# which is why mutable objects should set __hash__ = None to mark them as unhashable.
#
# >>> from mixin import ComparableMixin
#
# >>> class Hashable(ComparableMixin):
#      def __init__(self, firstname, lastname):
#          self._first = firstname
#          self._last = lastname
#
#      def _cmpkey(self):
#          return (self._last, self._first)
#
#      def __repr__(self):
#          return "%s(%r, %r)" % (self.__class__.__name__,
#                                 self._first, self._last)
#
#      def __hash__(self):
#          return hash(self._cmpkey())
#
# >>> d = {Hashable('Donald', 'Duck'): 'Daisy Duck'}
# >>> d
# {Hashable('Donald', 'Duck'): 'Daisy Duck'}
# #The attributes of this class are marked as internal by the convention of using a leading
# #underscore, but they are not strictly speaking immutable. If you want a truly immutable
# # class in Python the easiest way is subclassing collections.namedtuple, but that is out of
# # scope for this book.
# ----------------
#
# parserator train name_data/labeled/labeled.xml,name_data/labeled/company_labeled.xml probablepeople
# -------
# check with Shahin on reason for this error accessing psycopg2 from mac laptop environment
# OperationalError: could not translate host name "den-gp2-master01.ch.int" to address: nodename nor servname provided, or not known
# on laptop;
#
# on linux compute server -
# TypeError: file must be a readable file-like object for COPY FROM; a writable file-like object for COPY TO.
#
# probable solution - try to open the file and pass file handle as an argument - eg - open(/path/to/filename)
# ------------------
# python inheritance -
# #best way to call a parent's method in a child is as follows -
#
# class Foo(Bar):
#     def baz(self, arg):
#         return super(Foo, self).baz(arg)
#
# #above return statement can also be introspected without class hardcoding as return super(self.__class__, self).baz(arg)
# ----------------
# use string templates for sql substitution in different demandforce and make_pairs(...) function-
#
# from string import Template
# msg = Template("$name has $n messages")
# print(msg.substitute(name="Dave",n=37)
# -------------
# python 3 - io module -
#
# lowest level class is FileIO,
# then 1 level higher is BufferedReader,
# then 1 level higher is TextIOWrapper
#
# -----------------
# socket sends should always be in binary - bytes, bytearrays in python3.
#
# Rules of thumb:
# • All outgoing text must be encoded (ascii)
# • All incoming text must be decoded
#
# s.sendall(resp.encode('ascii'))
# ------------------------------
# to introspect (==java reflection) function arguments from within the same function, use
# inspect.currentframe().f_code.co_name
# http://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback/5067654#5067654
# #-----------------------------------------------------------------------------
# #introspect current module name from within module for logging purposes -
# #sets up logging.yaml
#
# import logging
# import os
# from logging.config import dictConfig
# import yaml
#
#
# def configure_logging():
#     logging_config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'logging.yml')
#     with open(logging_config_file, 'r') as f:
#         logging_config_dict = yaml.load(f)
#     dictConfig(logging_config_dict)
#
# configure_logging()
#
# LOG = logging.getLogger(__name__)
# ----------
# how to print logging from modules you want and disable logging from other external 3rd party libraries - define a logger by name and get that logger
#
#https://stackoverflow.com/questions/35325042/python-logging-disable-logging-from-imported-modules
#logger = logging.getLogger('my_module_name') - do this, it doesnt call the root logger but your specific logger
#Obviously you have to use logger.debug instead of logging.debug since the latter is a convenience function that calls the debug method of the root logger.
#
#This is mentioned in the Advanced Logging Tutorial. It also allows you to know which module triggered the log message in a simple way.
#
#
# variable argument substitution within exceptions thrown -
#
# if query_res == []:
#             raise ValueError("Could not find table %s.%s" % (table_namespace, relation_name))
# ----------
# os.path.dirname(__file__)
# ------------
# to extract all values (value set) from a list of hashes (dicts or key value pairs) for the same key , ie
# to convert this data structure
# results_q = [{'table_name': u'anti_transparency_list'},
#  {'table_name': u'anti_transparency_providers'},
#  {'table_name': u'insurance_company_data_files'},
#  {'table_name': u'icf_icdf_applied'}]
#
# into a list like
#
# ['anti_transparency_providers',
#  'anti_transparency_list',
#  'insurance_company_data_files',
#  'icf_icdf_applied']
#
# do this -
# table_names = [r['table_name'] for r in results_q]
#
# ---------------
# python to time how long modules took to run specific code blocks -
import datetime
start = datetime.datetime.now()
end = datetime.datetime.now()
elapsed_time = end - start
# ----------
# http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
# CamelCase converted to snake_case as per postgres and python PEP8 standard recommendations.
# -------
# #pep8 doc string comments -
# def my_function():
# """doc string in triple double-quotes like this"""
#   pass
#
# #-----------------------------------------
#
#
# --------------
# #using SQLAlchemy/ alembic to manage DB migrations within python
# #To create a migration to create table accounts, run a command like:
"""
alembic revision -m "create account table"
"""
#
# #if alembic complains about multiple heads, do the following
"""
alembic revision -m "add column provider_type to facility_test_data" --head=unlabeled_test_data@head
"""
#
# Then edit the new migration python file created under alembic/versions to issue the right
# commands to db to create table.
#
# #Then run (from within inner provider_matching directory):
"""
python migrations/migrate.py -u #(for unlabeled_test_data)
python migrations/migrate.py -u -d='33e95fab86da' #for downgrade on unlabeled_test_data path.
"""
#
# #run all migrations within a directory heirarchy
"""
python migrations/migrate.py --labeled_test_data
python migrations/migrate.py -l
"""
# #INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# #INFO  [alembic.runtime.migration] Will assume transactional DDL.
# #INFO  [alembic.runtime.migration] Running upgrade  -> 808af488b1ed, create alembic version table
# #INFO  [alembic.runtime.migration] Running upgrade 808af488b1ed -> 40c06f5d1065, create labeled_set table
# #INFO  [alembic.runtime.migration] Running upgrade 40c06f5d1065 -> 5f094727f37c, create provider_location_representations table
# #INFO  [alembic.runtime.migration] Running upgrade 5f094727f37c -> bfa1932030c6, create labeled_provider_location_pairs table
# #INFO  [alembic.runtime.migration] Running upgrade bfa1932030c6 -> 9edaf1839b84, create data_source table
#
#
# ------------------
# #callback functions -
#
#     def actions(self):
#         list = [
#             ['label', self.label_pairs],
#             ['train', self.train_model],
#             ['settings', self.print_model_settings],
#             ['verify', self.detect_training_duplicates],
#             ['test', self.detect_testing_duplicates],
#             ['all', self.detect_all_testing_duplicates],
#             ['save_threshold', self.save_threshold],
#             ['augment', self.augment_training_set],
#             ['tsv', self.save_training_as_tsv],
#         ]
#         return OrderedDict(list)
#
#     def execute_action(self, action):
#         self.actions()[action]()
# ---------------------
# #variable interpolation while raising exceptions in python 2 -
# raise ValueError("cbsa name '{0}' not found, or multiple cbsas found. Please enter a valid & unique cbsa name"
#                              .format(input_cbsa_name))
# --------------------------------------------
# #to run stand alone unit test in python
"""python -m unittest test_module.TestClass.test_method
python -m unittest tests.training_set_generator.test_data_interface_test.TestDataInterfaceTest.test_duplicate_or_invalid_cbsa_name_is_handled
"""
#
# Ran 1 test in 0.129s
#
# OK
#
"""python -m unittest tests.sql.custom_functions_test.CustomFunctionsTest"""
#
# Ran 4 tests in 0.072s
#
# OK
#
# to run all tests under tests/ directory -
"""python -m unittest discover -s tests/"""
#--------------DJANGO SPECIFIC NOTES BELOW ***************************
# unit testing in django - 
"""
python manage.py test adm
python manage.py test --verbosity 2 adm/tests/test_rule_estimates.py

./manage.py test --pattern="tests_*.py"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
"""

"""
python ./manage.py runserver 0.0.0.0:8080

python ./manage.py shell
# this is extremely useful for handling complex nested objects and a REPL to experiment around
"""

# adds a django migration under the app "common" and names the migration "add_waffle_flags_for_new_feature"
# manage.py makemigrations common --empty --name add_waffle_flags_for_new_feature

# apply migrations
# ./manage.py migrate <app_name>  # to migrate an individual app
import django
django.VERSION
# 1.8.14 is krux's django version

# --------------------------------------------END DJANGO SPECIFIC NOTES *************
# in python function taking **kwargs argument, keys that are non-strings are not allowed, like int
# keys.
# so just pass in a dictionary as a regular argument and not as a **kwargs
#
# # in python 2.7, int (integer) is represented by 63 bits.
sys.maxint
# gives the max value of int
#
# number of bits needed to represent this in binary is given by
sys.maxint.bit_length()
#
# #similarly,
# long.bit_length()
#
# #left pad to 8 bits in binary - using string formatter and removing the 0b string prefix
# #https://docs.python.org/2/library/string.html#grammar-token-width
# format(int(raw_input().strip(), 16), '08b')
#
# #right justify a string by left padding with zeros
a = '1'
num_chars_to_pad = 3
a.rjust(num_chars_to_pad, '0')  # returns '001'
#
# since string is immutable, you cannot try to mutate it while iterating over it like
b_4digit_binary = '1010'
j = 0
b_4digit_binary[j] = '0'
# TypeError: 'str' object does not support item assignment
# #------------------------------------------------------#------------------------------------------------------
# integer will never overflow in python (both python 2 and python 3)
# although int is of fixed precision, sys.maxint + 1 gets promoted to long which is arbitrary
# precision
# sys.maxsize can be used when you need an arbitrarily large value
# Python has arbitrary precision integers so there is no true fixed maximum. You're only limited by
# available memory.
#
# In Python 2, there are two types, int and long.  ints use a C type, while longs are arbitrary
# precision. You can use sys.maxint to find the maximum int. But ints are automatically promoted to
# long, so you usually don't need to worry about it:
#
# sys.maxint + 1
# works fine and returns a long.
#
# sys.maxint does not even exist in Python 3, since int and long were unified into a single
# arbitrary precision int type.
#
# Python uses the larger integer type avaiable for the machine. SO usually on 32-bit machines int
# will have 32bit size, while on 64 bit-machines it will have 64 bit size. But there could be 32-bit
# architectures defining 64 bit integers, in that case python would use the 64-bit integer
# #------------------------------------------------------#------------------------------------------------------
# #python string equality
# http://stackoverflow.com/questions/1504717/why-does-comparing-strings-in-python-using-either-or-is-sometimes-produce
# a == b returns if a ==b
# but if a is b returns if id(a) == id(b)
# ------------------------
# #flatten a list of dictionary hashes
# # [{'id': 2}, {'id': 3}, {'id': 4}]
# # to [2,3,4]
# --------------
# #substrings in python
# myString[2:end]
# --------------
# #list append
# a = []
#
# High speed is retained by preferring vectorized building blocks over the use of for-loops and
# generators which incur interpreter overhead.
# The superior memory performance is kept by processing elements one at a time rather than bringing
# the whole iterable into memory all at once.
# Code volume is kept small by linking the tools together in a functional style which helps
# eliminate temporary variables.
# https://docs.python.org/2.7/library/itertools.html#recipes
# use itertools for random iteration of variable length conditional increments
# ----------------
# #running dbcopyutil to load data from greenplum into mysql
# #setup virtualenv on signoff machine, install all duplo dependencies within it
#
# #dbcopy/conf/pg2mysql.yml - has cfgs for db connectivity
#
# #python pg2mysql/pg2mysql.py
# ----------------------
# import pandas
# train_data.describe(include= 'all')
# ---------------
# to run code coverage - either use the nose package , or
# py.test --cov=mies.dataimport.npi.npi_raw_loader tests/mies/dataimport/npi/npi_raw_loader_test.py
#------
"""
pip install nose 
pip install coverage

nosetests --with-coverage --cover-erase --cover-package=match.run.provider_cluster
"""
# -------------------
# #python data structure performance speed - set is fastest while list is slowest
# # set >> tuple > list
# ---------------------
# a.insert(bisect.bisect_left(a, x, lo, hi), x)
# #to insert into a sorted array and keep it sorted; bisect finds the index where to insert - O(log n) operation
# #inserting into the array is an O(n) operation
# ---------------------
# pypy is a jit (just in time) compiler for python code
# -----------
# pySpark known limitations:
#   a) IO thruput - python to spark (1.15 MBps), spark to python (9.82 MBps) (or python extension code)
#     this can be improved  to 25 MBps by using pickled data frames in pandas and then pushing it
# down to spark and appending it to RDD
#     https://www.youtube.com/watch?v=abZ0f5ug18U&list=PL-x35fyliRwiz70bTSSK4HmOZ4JazCFUj&index=7
#
#   b) running interpreted python code on RDDs / Spark DataFrames
#     i) lambda mappers / reducers (rdd.map(...)
#     ii) Spark SQL UDFs (registerFunction(...) )
#
# eg -
# rdd = sc.parallelize(arr) #pySpark with lambda function; uses 8 cores
#
# def f(x):
#     return x * 2
#
# %timeit rdd.map(f).sum()
#
# is 100x slower than
# timeit (arr * 2).sum() # numpy; runs on single core
#
# # Lesson learnt: python data analytics should not be based around scalar object iteration
# -----------------------------------
# # The PEP8 recommended way to check if a stack is empty -
# # For sequences, (strings, lists, tuples), use the fact that empty sequences are false.
# Yes: if not seq:
#      if seq:
#
# No:  if len(seq):
#      if not len(seq):
# #------------------------------------------------------------------------
# # TODO: min Queue in python
# # http://www.keithschwarz.com/interesting/code/?dir=min-queue
#
# # http://www.dabeaz.com/usenix2009/concurrent/
# # 2009 talk on concurrency with code. TODO
#
# # concurrency talk by David Beazley at pycon 2015
# # https://www.youtube.com/watch?v=MCs5OvhV9S4
# # https://github.com/dabeaz/concurrencylive/blob/master/server.py
#
# # socket server multithreaded connecting with 2 clients concurrently using threads and computing
# fibonacci.
# # GIL prioritizes things that want to run on the CPU core
# # OS gets priority to short running tasks
# # response times for longer tasks will become exponentially slow. The solution is to throw the
# work out to a Process pool. in python 3,
# from concurrent.futures import ProcessPoolExecutor as Pool
# future = pool.submit(fib, n)
#
# #threads solve the problem of blocking - waiting for data, send buffer is full, etc.
# Blocking prevents concurrency.
def countdown(n):
    while n > 0:
        yield n
        n -= 1

c = countdown(5)
next(c)  # 5

for i in c:
    print(i)
# 4\n3\n2\n1
#
# #--
# # round robin task scheduler - using yield(generator) coroutines
from collections import deque
from select import select
from app.concurrency.count_down_latch import CountDownLatch
tasks = deque()
tasks = [CountDownLatch(5), CountDownLatch(10), CountDownLatch(20)]
def run():
    while tasks:
        task = tasks.popleft()
        try:
            next(task)  # run to the yield
        except StopIteration:
            print("task done")
#--
# python wait on I/O from sockets using `select` library
recv_wait = {} # mappings sockets -> tasks (generators)
send_wait = {}
def run():
    while any([tasks, send_wait, recv_wait]):
        while tasks:
            # no active tasks to run, wait for I/O
            can_recv, can_send = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
# #---
# #class that wraps around socket object; provides alternate impl of recv and send calls


class AsyncSocket(object):
    def __init_(self, sock):
        self.sock = sock

    def recv(self, maxsize):
        yield 'recv', self.sock
        # return self.sock.recv(maxsize)
        #  `return` with arg in generator works only in python > 3.3

    # sub-routine hidden behind a method
    def send(self, data):
        yield 'send', self.sock
        # return self.sock.send(data) # `return` with arg in generator works only in python > 3.3

    def accept(self):
        yield 'recv', self.sock
        client, addr = self.sock.accept()
        # return AsyncSocket(client), addr
        #  `return` with arg in generator works only in python > 3.3

    def __getattr__(self, name):
        return getattr(self.sock, name)
# coroutines much more efficient than posix threads if you want 50k parallel clients
# twisted library for async callbacks
# #------
# # https://www.youtube.com/watch?v=Bv25Dwe84g0
# # Raymond Hettinger talk in 2016 about concurrency. TODO
# #-------
#python3 virtual environment
"""
pyvenv py3_kur
source myenv/bin/activate
"""
# #------------
# #custom comparator or custom sorting in python  - secondary sort
from operator import itemgetter, attrgetter, methodcaller


class Student:
    def __init__(self, name, grade, age):
            self.name = name
            self.grade = grade
            self.age = age

    def __repr__(self):
            return repr((self.name, self.grade, self.age))

    def weighted_grade(self):
            return 'CBA'.index(self.grade) / float(self.age)

# [(student.name, student.weighted_grade()) for student in student_objects]
student_objects = [('john', 0.13333333333333333), ('jane', 0.08333333333333333), ('dave', 0.1)]
sorted(student_objects, key=methodcaller('weighted_grade'))
# [('jane', 'B', 12), ('dave', 'B', 10), ('john', 'A', 15)]

#
# # Both list.sort() and sorted() accept a reverse parameter with a boolean value.
# # This is using to flag descending sorts. For example, to get the student data in reverse age order
# sorted(student_tuples, key=itemgetter(2), reverse=True)
#
# # in python3, `cmp` parameter to lst.sort() and sorted(<iterable>) is completely removed as it was slow. key-based sorting is fastest
# # for porting python2 code using cmp to python3 which uses only key, use the following template provided by Raymond Hettinger
# # https://wiki.python.org/moin/HowTo/Sorting/
#
# # To create a standard sort order for a class, just add the appropriate rich comparison methods:
# >>> Student.__eq__ = lambda self, other: self.age == other.age
# >>> Student.__ne__ = lambda self, other: self.age != other.age
# >>> Student.__lt__ = lambda self, other: self.age < other.age
# >>> Student.__le__ = lambda self, other: self.age <= other.age
# >>> Student.__gt__ = lambda self, other: self.age > other.age
# >>> Student.__ge__ = lambda self, other: self.age >= other.age
# >>> sorted(student_objects)
# [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
# #For general purpose comparisons, the recommended approach is to define all six rich comparison operators.
# # The functools.total_ordering class decorator makes this easy to implement.
#
# # Key functions need not access data internal to objects being sorted.
# # A key function can also access external resources.
students = ['dave', 'john', 'jane']
newgrades = {'john': 'F', 'jane':'A', 'dave': 'C'}
sorted(students, key=newgrades.__getitem__) # ['jane', 'dave', 'john']
# #---------------------------------------
# # Notes about square root function in python 2.0 - its usually done as 9**(1/2.0)
# # ie, sqrt of x is syntactically computed as x ** (1/2.0). The resulting number is a float.
# # The float type has a method is_integer() which is True of its an integer, false otherwise.
#
(9**(1/2.0)).is_integer()  # Returns True
(8**(1/2.0)).is_integer()  # Returns False

-------
# pip install from local egg file not in pypi index
# pip install --no-index --find-links=/opt/program/libs sa-models

# to package sa-models whl - 
# python3 setup.py sdist bdist_wheel

#------------------------
# pandas join example merge
def join_data_with_embeddings():
    import turicreate as tc
    import pandas as pd
    sf = tc.SFrame.read_csv("sample_data.csv", header=True, delimiter=',')
    df = sf.to_dataframe()
    # print(df["image_url_x"][0])
    df["image_name"] = df["image_url_x"].map(get_image_name_from_path)
    # print(df["image_name"][0])
    import pickle
    with open("image_embeddings.txt", 'rb') as f:
        image_name_to_embeddings_map = pickle.load(f)
    d = {
            'image_name': list(image_name_to_embeddings_map.keys()),
            'image_embedding': list(image_name_to_embeddings_map.values())
         }
    embeddings_df = pd.DataFrame.from_dict(d, orient="columns")
    return pd.merge(df, embeddings_df, on='image_name', how='left')


def get_image_name_from_path(path: str):
    """

    :param path: input like https://lsco.scene7.com/is/image/lsco/dockers/clothing/863380001-front-pdp.jpg?$grid_desktop_full$
    :return: 863380001-front-pdp.jpg
    """
    return path.split("/")[-1].split("?")[0]

# pandas sample a data frame
df['image_embedding'].sample(n=3, random_state=1)

# pandas filter by null
filtered_df = df[df['image_embedding'].isnull()]
#------------------------------------------
# pandas select t.x from t where t.y = 'A'
df["image_url_x"].where(df["product_id"]=="274060059")
# this replaces non-matching columns with NaN and returns the entire columnar data, not what we want

#below is what we want
df.loc[df['product_id'] =="274060059", ['image_url_x']].iloc[0].astype(str)
# returns the 1st match among all rows as an object, typecast as a string

df.loc[df['product_id'] =="274060059", ['image_url_x']] returns a series while
df.loc[df['product_id'] =="274060059", 'image_url_x'] returns a str

#------------------------------------------
# code to display images in jupyter notebook
from IPython.display import Image, display
from IPython.core.display import HTML
import ipyplot
for index in [43, 494, 127, 41, 302, 709, 737, 744, 47]:
    product_id = index_to_item[index]
    image_url = df.loc[df['product_id'] == product_id, 'image_url_x'].iloc[0].split("?")[0]
    display(Image(image_url, width=400, height=400))

#------------------------------------------

df.info()
# gives summary of nulls on pandas dataframe

# pandas fill nulls with 0
for col in ["snds_opens_dec", "hard_sale_price"]:
    df2[col].fillna(value=0,inplace=True)

# create new virtual environment in python3
python3 -m venv /path/to/new/virtual/environment
# note that venv doesnt let you use different python3 versions, for that use virtualenv
virtualenv --python=/usr/bin/python2.6 <path/to/new/virtualenv/>
