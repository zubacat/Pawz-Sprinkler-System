#!/usr/bin/env python3
import time
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')