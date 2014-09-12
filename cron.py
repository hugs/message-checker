""" main.py is the top level script.
"""

import os
import sys
import json
import logging
from message import Message

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import Response
from flask import url_for
from flask import session
app = Flask(__name__.split('.')[0])

import datetime
def seconds_ago(time_s):
    return datetime.datetime.now() - datetime.timedelta(seconds=time_s)
    
@app.route('/admin/delete-old-messages') 
def delete_old_messages():
    #messages = Message.query(Message.address == "joe").fetch(10)    
    messages = Message.query().filter(Message.date > seconds_ago(6*60*60))
    for message in messages:
        logging.info(message.uuid)
