# -*- coding: utf-8 -*-
"""

    Flask-shrtn
    ~~~~~~~~~~~

    A URL shortener writen in Python using 
    Flask microframework and jessex's shrtn.

    :copyright: (c) 2011 by Josh Finnie.
    :license: MIT, see README for more details.

"""
from datetime import datetime
import sys, re, zlib
from urlparse import urlparse

ALPHABET = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
DOMAIN = "http://jfin.us/s/"
re_short = re.compile(DOMAIN + "[a-kmnop-zA-HJ-NP-Z2-9]+$")
re_end = re.compile("[.][^/]+$")

from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.wtf import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

"""
    jessex's code found at https://github.com/jessex/shrtn. Below is an edited 
    version to work with Flask-shrtn.
"""

# ****************************** SHRTN BEGINS **********************************
# ****************************** HELPER FUNCTIONS ******************************

def is_valid_short(url):
    """
        Takes in a url and determines if it is a valid shortened url.
    """
    return not (not re_short.match(url))

def standardize_url(url):
    """
        Takes in a url and returns a clean, consistent format. For example:
        example.com, http://example.com, example.com/ all are http://example.com/
        Returns None if the url is somehow invalid.
    """
    if is_valid_short(url): #will not shorten one of our already shortened URLs
        return None
    parts = urlparse(url, "http") #default scheme is http if omitted
    if parts[0] != "http" and parts[0] != "https": #scheme was not http(s)
        return None

    #url appears valid at this point, proceed with standardization
    standard = parts.geturl()
    #work-around for bug in urlparse
    if standard.startswith("http:///") or standard.startswith("https:///"):
        standard = standard.replace("///", "//", 1) #get rid of extra slash
    if not standard.endswith("/"): #does not end with '/'...
        if re_end.findall(standard): #...but ends with .something...
            if parts[0] == "http":
                bound = 7
            elif parts[0] == "https":
                bound = 8
            if standard.rfind("/", bound) == -1: #...and contains no other '/'
                return standard + "/" #append a '/'
    return standard


# ******************************* CORE FUNCTIONS *******************************

def create_short_url(long_url):
    standard_url = standardize_url(long_url)

    if standard_url is None:
        return "An Error has occured"

    num = zlib.crc32(standard_url)

    if num < 0:
        num = (long(num) + 4294967296L)

    if (num == 0):
        print ALPHABET[0]

    arr = []
    base = len(ALPHABET)

    while num:
        rem = num % base
        num = num // base
        arr.append(ALPHABET[rem])

    arr.reverse()
    short_url = ''.join(arr)

    return DOMAIN+short_url

# ****************************** SHRTN ENDS ************************************

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
    form = URL_Shortener
    return render_template('index.html', form=form)

@app.route('/add', methods=['POST'])
def add_url():
    if request.method =='POST':
        if not request.form['url']:
            flask('URL is required.')
        if not request.form['short_url']:
            url = URL(request.form['url'])
            db.session.add(url)
            db.session.commit()
            flash('URL was properly shortend')
            return redirect(url_for('show_url'))
        else:
            url = URL(request.form['url'], request.form['short_url'])
            db.session.add(url)
            db.session.commit()
            flash('URL was properly shortend')
            return redirect(url_for('show_url'))
    flash('New entry was successfully posted')

@app.route('/show_url')
def show_url():
    for url in URL.query.find()

@app.route('/<url_id>')
def reroute(url_id):
    full_url = lengthen_url(url_id)
    return redirect(full_url)

if __name__ == '__main__':
    app.run()
