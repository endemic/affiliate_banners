import cherrypy
from cherrypy.test import helper
from server import WebApp

class WebAppTest(helper.CPWebCase):
    @staticmethod
    def setup_server():
        # TODO: set up test database here
        cherrypy.tree.mount(WebApp())

    def test_redirect(self):
        self.getPage('/follow/1')
        self.assertStatus('303 See Other')
        self.assertHeader('Location', 'https://ganbarugames.com')

    def test_get_content(self):
        self.getPage('/')
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'application/json')
        # Best way to test the body?
