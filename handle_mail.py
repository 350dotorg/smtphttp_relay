import logging, email
from google.appengine.ext import webapp 
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
import urllib

class MailReceiver(InboundMailHandler):
    def post(self, to):
        self.receive(mail.InboundEmailMessage(self.request.body), urllib.unquote(to))

    def receive(self, msg, to):
        msg.original.add_header("X-Original-To", msg.original.get("To"))
        msg.original.replace_header("To", to)
        mime_message = msg.original.as_string()
        logging.info(mime_message)
        taskqueue.add(url='/process_mail',
                      params={'mime_message': mime_message})

import wsgiref.handlers
application = webapp.WSGIApplication([
        ('/_ah/mail/(.+)', MailReceiver)
        ], debug=True)
wsgiref.handlers.CGIHandler().run(application)
