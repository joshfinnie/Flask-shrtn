# Flask-shrtn
## Description
### What is Flask?
Flask is a microframework for Python based on Werkzeug
and Jinja2.  It's intended for small scale applications
and was developped with best intentions in mind.

Find out more at [http://flask.pooco.org](http://flask.pooco.org) 
or [https://github.com/mitsuhiko/flask](https://github.com/mitsuhiko/flask)

### What is shrtn
shrtn is a project to satisfy a personal curiosity: learning what's under the 
hood of URL shortening services. The best way to learn (for some of us) is to 
actually do, so I decided to write a URL shortening engine in my favorite 
language, without actually intending to place it online because there is such 
a glut of URL shorteners on the web that it hardly seems worth it.

Find out more at [https://github.com/jessex/shrtn](https://github.com/jessex/shrtn)

### What is Flask-shrtn
Flask-shrtn is a full-fledged website that can be run on a server that will
give you the ability to shorten our own URLs.  It uses the technology of the
Flask microframework and jessex's shrtn code.

## Instructions
>$ easy-install Flask
>$ easy-install Flask-SQLAlchemy
>$ easy-install Flask-WTF
>$ git clone git://github.com/joshfinnie/Flask-shrtn.git
>$ python Flask-shrtn.py
>  * running on http://localhost:5000/

## License
Copyright (C) 2011 by Josh Finnie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
