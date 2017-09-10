from datetime import datetime
import pandas as pd
from flask import Flask, abort, flash, redirect, render_template, request, url_for


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html', title='Landing!')

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run()