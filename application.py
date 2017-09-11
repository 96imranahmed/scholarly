from datetime import datetime
import pandas as pd
import numpy as np
from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify

import pickle
from search import search

application = Flask(__name__)
search_arr = pickle.load(file = open('./search_array.pickle', 'rb'))

@application.route('/')
def main():
    return render_template('index.html')

@application.route('/search/')
def search_decorator():
    query = request.args.get('term')
    return jsonify(search(query, search_arr, 0, 10))

@application.route('/paper/<query>')
def four_or_four(query):
    return "<h2>Thanks for dropping by, this functionality is coming very soon!</h2>"

@application.route('/author/<query>')
def four_or_four_two(query):
    return "<h2>Thanks for dropping by, this functionality is coming very soon!</h2>"
# run the application.
if __name__ == "__main__":
    application.debug = False
    application.run()