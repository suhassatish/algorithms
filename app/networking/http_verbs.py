"""
A basic HTTP request consists of:

1) A verb (or method)
2) A resource (or endpoint)

Verb	Meaning	 Idempotent 	 Safe 	 Cacheable
GET	Reads a resource	Yes	Yes	Yes
POST	Creates a resource or triggers a data-handling process	No	No	Only cacheable if response
contains explicit freshness information
PUT	Fully updates (replaces) an existing resource or create a resource	Yes	No	No
PATCH	Partially updates a resources	No	No	Only cacheable if response contains explicit
freshness information
DELETE	Deletes a resource	Yes	No	No

The table above shows only the HTTP verbs used commonly by RPC and REST APIs.
"""
