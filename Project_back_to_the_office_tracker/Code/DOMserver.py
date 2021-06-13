"""Server for back to the office tracker app."""

from flask import (Flask, render_template, request, flash, session, redirect, url_for, jsonify)
from model import connect_to_db, Office
import crud
from sample import geocode
from jinja2 import StrictUndefined
from json import dumps



app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def sample():
    return render_template('DOM_sample.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)