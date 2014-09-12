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

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/check/')
def check(address=None):
    address = request.args.get('address', None)
    if address:
        return redirect(url_for('messages', address=address))
    else:
        return redirect(url_for('main'))

@app.route('/address/<address>')
def messages(address=None):
    if address:
        if address.endswith('@message-checker.appspotmail.com'):
            address = address.split('@message-checker.appspotmail.com')[0]
        
        try:
            messages = Message.query(Message.address == address).fetch(10)
        except ValueError:
            messages = []
    else:
            messages = [] 

    return render_template('messages.html', address=address, messages=messages)

@app.route('/address/<address>/messages.json')
def messages_json(address=None):
    try:
        messages = Message.query(Message.address == address).fetch(10)
    except ValueError:
        messages = []

    serializable_messages = [[message.uuid, message.subject, message.date.strftime('%I:%M %p')] for message in messages]

    return Response(json.dumps(serializable_messages), mimetype='application/json')

@app.route('/message/<uuid>')
def message(uuid=None):
    try:
        message = Message.query(Message.uuid == uuid).get()
    except ValueError:
        pass

    if message:
        return render_template('message.html', message=message)
    else:
        return render_template('404.html'), 404

@app.route('/message-body/<uuid>')
def message_body(uuid=None):
    try:
        message = Message.query(Message.uuid == uuid).get()
    except ValueError:
        pass

    if message:
        if message.html:
            return message.html
        else:
            return message.plain_text
    else:
        return render_template('404.html'), 404

@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html'), 404