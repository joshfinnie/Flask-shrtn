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
import sys, re
from urlparse import urlparse

ALPHABET = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
DOMAIN = "http://s.jfin.us"
re_short = re.compile(DOMAIN + "[a-kmnp-zA-HJ-NP-Z2-9]+$")
re_end = re.compile("[.][^/]+$")

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.wtf import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

""" jessex's code found at https://github.com/jessex/shrtn. Below is an edited 
version to work with Flask-shrtn."""

# ****************************** SHRTN BEGINS **********************************
# ****************************** HELPER FUNCTIONS ******************************

def is_valid_short(url):
	"""Takes in a url and determines if it is a valid shortened url."""
	return not (not re_short.match(url))

def standardize_url(url):
	"""Takes in a url and returns a clean, consistent format. For example:
	example.com, http://example.com, example.com/ all are http://example.com/
	Returns None if the url is somehow invalid."""
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

def shorten_url(url, conn):
	"""Takes in a standard url and returns a shortened version."""
	url = standardize_url(url)
	if url is None: #tried to shorten invalid url
		return None

	#get the id for this url (whether new or otherwise)
	id = db.search_url(url, db.MYTABLE, conn)
	if not id: #url not yet inserted into database
		id = db.insert_url(url, db.MYTABLE, conn) #insert and get its id

	code = convert_to_code(id)
	return "%s%s" % (DOMAIN, code)

def lengthen_url(url, conn):
	"""Takes in one of our shortened URLs and returns the correct long url."""
	#isolate code from shortened url
	if not is_valid_short(url): #url was not constructed properly
		return "%s404" % DOMAIN
	code = url[14:] #just the code, ie. h7K9g0

	id = resolve_to_id(code) #convert shortened code to id
	long = db.search_id(id, db.MYTABLE, conn)
	if not long: #id was not found in database
		return "%s404" % DOMAIN #issue 404
	return long #url to perform 301 re-direct on

def convert_to_code(id, alphabet=ALPHABET):
	"""Converts a decimal id number into a shortened URL code. Use the id of the
	row in the database with the entered long URL."""
	if id <= 0: #invalid codes (autoincrement is always 1 or higher)
		return alphabet[0]

	base = len(alphabet) #base to convert to (56 for our standard alphabet)
	chars = []
	while id:
		chars.append(alphabet[id % base])
		id //= base
	chars.reverse() #moved right to left, so reverse order
	return ''.join(chars) #convert stored characters to single string

def resolve_to_id(code, alphabet=ALPHABET):
	"""Converts the shortened URL code back to an id number in decimal form. Use
	the id to query the database and lookup the long URL."""
	base = len(alphabet)
	size = len(code)
	id = 0
	for i in range(0, size): #convert from higher base back to decimal
		id += alphabet.index(code[i]) * (base ** (size-i-1))
	return id

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
            flask('URL is required.)
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
