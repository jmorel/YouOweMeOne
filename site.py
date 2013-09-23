import sys
import cherrypy

class Root:
        @cherrypy.expose
        def index(self):
                return 'Hello, this is your default site.'

cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 14902,
})
cherrypy.quickstart(Root())
