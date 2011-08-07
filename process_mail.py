import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
import urllib
import base64
from django.utils import simplejson as json

class MailProcessor(webapp.RequestHandler):
    def post(self):
        mime_message = self.request.get("mime_message")
        data = base64.b64encode(mime_message)
        rpc = urlfetch.create_rpc()
        urlfetch.make_fetch_call(
            rpc, "http://localpower.socialplanning.org/_inbound_mail/", 
            payload=data, method=urlfetch.POST,
            headers={'Content-Type': "text/plain"})

app = webapp.WSGIApplication([
        ('/process_mail', MailProcessor),
        ], debug=True)
run_wsgi_app(app)
