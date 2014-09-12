import logging
import uuid
import webapp2
from message import Message
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

class LogSenderHandler(InboundMailHandler):
    def receive(self, message):
        url = self.request.path
        to = url.split('/')[-1]
        address = to.split('@')[0]

        unique_id = str(uuid.uuid4())

        logging.info("================================")
        logging.info("From: " + message.sender)
        logging.info("To: " + to)
        logging.info("Address: " + address)
        logging.info("Subject: " + message.subject)
        logging.info("Date: " + message.original.get('Date'))
        logging.info("ID: " + unique_id)

        plaintext_bodies = message.bodies('text/plain')
        plaintext_body = ''
        if plaintext_bodies:
            for content_type, encoded_body in plaintext_bodies:
                logging.info("Content_type: " + content_type)
                plaintext_body = encoded_body.payload
                logging.info("Body: " + plaintext_body)

        html_bodies = message.bodies('text/html')
        html_body = ''
        if html_bodies:
            for content_type, encoded_body in html_bodies:
                html_body = encoded_body.decode()

        stored_message = Message()
        stored_message.uuid = unique_id
        stored_message.sender = message.sender
        stored_message.to = to
        stored_message.address = address
        stored_message.subject = message.subject
        stored_message.plain_text = plaintext_body
        stored_message.html = html_body
        stored_message.put()

        logging.info("================================")

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)