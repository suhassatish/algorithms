"""
Design a request dispatcher for a web-server that accepts and processes incoming web requests
concurrently and responds synchronously. How can this design be modified to support asynchronous
response?

https://www.quora.com/How-do-I-design-a-request-dispatcher-for-load-balancing


Flask is a good choice in python for a REST API because it has RESTful request dispatching.
read http://blog.luisrei.com/articles/flaskrest.html

Asynchronous request dispatcher application design considerations
https://www.ibm.com/support/knowledgecenter/SSAW57_8.5.5/com.ibm.websphere.nd.doc/ae/rweb_ard_considerations.html
To prevent unauthorized results access, unique IDs are generated for the service URI and for the
Asynchronous Request Dispatcher entries. A common ID generator is shared among the session and ARD,
so uniqueness is configurable through session configuration. Session IDs are considered secure,
but they are not as secure as using a Lightweight Third-Party Authentication (LTPA) token.

When making a request to the endpoint, ARD sends as many response fragments as possible when the
request is made. Therefore, the client needs to re-request if all fragments are not initially
returned. Trying to display the results directly in a browser without using an XMLHttpRequest
can result in errors related to non well-formed XML.

If the ARD work manager runs out of worker threads (from its thread pool to serve requests),
the request is processed like a synchronous request.

TODO - related. Load balancer design
http://www.haproxy.org/
simple round robin scheduling is the simplest algorithm for load balancing & request dispatch
scheduling. Consistent hashing is better though, if you were to add an extra processing node,
only a small fraction of users have to be reallocated to the new processing node.

3 important factors used to measure a load balancer's performance -
1) session concurrency - number of concurrent simultaneous users
2) session rate - requests per second
3) data forwarding rate - MBps downloaded
"""
import cherrypy


class Root(object):

    @cherrypy.expose
    def index(self):
        return 'Hello world'


class RestAPI(object):

    exposed = True

    def POST(self):
        return 'post'

    def GET(self):
        return 'get'


cherrypy.config.update({
    'global': {
        'environment': 'test_suite',
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    }
})

cherrypy.tree.mount(Root())

cherrypy.tree.mount(RestAPI(), '/api',
    {'/':
        {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    }
)

cherrypy.engine.start()
cherrypy.engine.block()

if __name__ == '__main__':
    # curl -X POST --header "Content-length: 0" http://localhost:8080/api
    pass
