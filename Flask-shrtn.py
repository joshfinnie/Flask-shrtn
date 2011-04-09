# -*- coding: utf-8 -*-
"""
    Flask-shrtn
    ~~~~~~

    A URL shortener using Flask and jessex's shrtn.

    :copyright: (c) 2011 by Josh Finnie.
    :license: MIT, see README for more details.
"""
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
