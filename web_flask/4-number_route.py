#!/usr/bin/python3
"""Flask module"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Greetings, hbnb project"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def textc(text):
    """Displays 'C' followed by the value of the text variable"""
    text = text.replace('_', ' ')
    return f"C {escape(text)}"


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def textpython(text='is cool'):
    """Displays 'Python' followed by the value of the text variable"""
    text = text.replace('_', ' ')
    return f"Python {escape(text)}"


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """displays “<n> is a number” only if n is an integer"""
    return f"{escape(n)} is a number"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
