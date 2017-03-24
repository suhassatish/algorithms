"""
BayPiggies Meetup @ LinkedIn by Senior Staff SWE @ Google - Mar 23, 2017
4th Thursday of every month - meetup running from late 90s

Jeff Fischer
aleax.it/pyconit17_en.pdf

https://martinfowler.com/articles/mocksArentStubs.html

How to test the database adapter?
Mocking out database is an option only if you understand the DB completely.
If the DB has a constraint s.t. after calling close() on connection,
any other query raises an Exception; then mocking it out will not accurately model this behaviour.

Here, you should use an emulation of a DB INSTEAD of mocking. There's a difference b/w the 2.

From python 3.X's unittest module, import mock.
If you run mock.patch.name, its easy to get misled.
Always better to use mock.patch.object instead.

If there's an in-memory look-up table map, make sure you have a smaller hash-map fake in your
test environment that is thorough and deep to mimic the actual semantics well, and has to be fast.

Aim for 80-90% code coverage (Google recommendation)
"""