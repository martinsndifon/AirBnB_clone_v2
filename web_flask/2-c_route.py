#!/usr/bin/python3
"""Flask module"""

from flask import Flask

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
    return f"C {text}"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
