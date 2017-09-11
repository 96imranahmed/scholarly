from datetime import datetime
import pandas as pd
import numpy as np
from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify

import pickle
from search import search

app = Flask(__name__)
search_arr = pickle.load(file = open('./search_array.pickle', 'rb'))

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search/')
def search_decorator():
    query = request.args.get('term')
    return jsonify(search(query, search_arr, 0, 10))

# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run()