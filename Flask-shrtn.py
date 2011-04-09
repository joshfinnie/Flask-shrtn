# -*- coding: utf-8 -*-
"""
    Flask-shrtn
    ~~~~~~

    A URL shortener using Flask and jessex's shrtn.

    :copyright: (c) 2011 by Josh Finnie.
    :license: MIT, see README for more details.
"""
from datetime import datetime

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.wtf import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    url_short = db.Column(db.String())
    pub_date = db.Column(db.DateTime)
 
    def __init__(url, url_short=None):
        self.url = url
        if url_short is None:
            url_short = create_url_short(url)
        self.url_short = url_short
        self.pub_date = datetime.utcnow()

class URL_Shortener(Form):
    url = TextField(url, validators=[Required()])
    short_url = TextField(short_url)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
