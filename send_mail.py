import base64
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class SendMail(webapp.RequestHandler):

    """
    Convenience view for using GAE as a mail-sending backend
    for a local development server to POST outbound mails to
    """
    def post(self):
        from_ = self.request.get("from_email")
        recipients = self.request.get("recipients").split(",")
        subject = self.request.get("subject")
        body = base64.decodestring(self.request.get("text"))
        html = base64.decodestring(self.request.get("html"))
        fields = dict(sender=from_,
                      to=recipients,
                      subject=subject,
                      body=body,
                      html=html)
        reply_to = self.request.get("reply_to")
        if reply_to and reply_to.strip():
            fields['reply_to'] = reply_to
        
        mail.send_mail(**fields)

        self.response.out.write("ok")

app = webapp.WSGIApplication([
        ('/_send_mail/', SendMail),
        ], debug=True)
run_wsgi_app(app)
