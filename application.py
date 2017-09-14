from datetime import datetime
import pandas as pd
import numpy as np
from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify

import pickle
from search import search

application = Flask(__name__)
p_loc, search_arr = pickle.load(file = open('./pickles/search_array.pickle', 'rb'))

@application.route('/')
def main():
    return render_template('index.html')

@application.route('/search/')
def search_decorator():
    query = request.args.get('term')
    return jsonify(search(query, search_arr, 0, 10))

@application.route('/paper/<query>')
def paper_decorator(query):
    return render_template('paper.html', search_term = search_arr[int(query) + p_loc][0])

@application.route('/author/<query>')
def author_decorator(query):
    return render_template('author.html', search_term = search_arr[int(query)][0].title())

# run the application.
if __name__ == "__main__":
    application.debug = False
    application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    application.run()