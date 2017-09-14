from datetime import datetime
import pandas as pd
import numpy as np
from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify

import pickle
from search import search

application = Flask(__name__)
search_arr = pickle.load(file = open('./pickles/search_array.pickle', 'rb'))
paper_id_title = pickle.load(file= open('./pickles/scholarly_id_paper_title.pickle', 'rb'))
author_id_name = pickle.load(file=open('./pickles/scholarly_id_user_name.pickle','rb'))

@application.route('/')
def main():
    return render_template('index.html')

@application.route('/search/')
def search_decorator():
    query = request.args.get('term')
    return jsonify(search(query, search_arr, 0, 10))

@application.route('/paper/<query>')
def paper_decorator(query):
    return render_template('paper.html', search_term = paper_id_title[int(query)])

@application.route('/author/<query>')
def author_decorator(query):
    return render_template('author.html', search_term = author_id_name[int(query)].title())

# run the application.
if __name__ == "__main__":
    application.debug = False
    application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    application.run()