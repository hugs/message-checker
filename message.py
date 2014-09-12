from datetime import datetime, date, time
from google.appengine.ext import ndb

class Message(ndb.Model):
    """Models an individual email message."""
    uuid = ndb.StringProperty(indexed=True)
    sender = ndb.StringProperty(indexed=False)
    to = ndb.StringProperty(indexed=True)
    address = ndb.StringProperty(indexed=True)
    subject = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    plain_text = ndb.StringProperty(indexed=False)
    html = ndb.StringProperty(indexed=False)
    original = ndb.StringProperty(indexed=False)