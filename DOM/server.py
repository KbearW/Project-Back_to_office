from flask import (Flask, render_template, request, flash, session, redirect, url_for, jsonify)

app = Flask(__name__)
app.secret_key = "dev"

@app.route('/')
def sample():
    return render_template('sample.html')