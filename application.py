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
    cur_item =  search_arr[int(query) + p_loc]
    months = ["Unknown", "January", "Febuary", "March", "April", "May","June",
              "July", "August", "September", "October", "November", "December"]
    desc = ', '.join(cur_item[4])
    date = datetime.utcfromtimestamp(cur_item[5])
    desc = '(' + months[date.month] + ' '  + str(date.year) +') ' + desc
    if len(desc) > 70:
        desc = desc[:desc.find(', ',40)] + " and others"
    return render_template('paper.html', title = cur_item[0], subtitle = desc)

@application.route('/author/<query>')
def author_decorator(query):
    cur_item = search_arr[int(query)]
    subtitle = " paper"
    if len(cur_item[3]) > 1:
        subtitle = str(len(cur_item[3])) + subtitle + 's'
    else:
        subtitle = 'One' + subtitle
    return render_template('author.html', title = cur_item[0].title(), subtitle= subtitle)

# run the application.
if __name__ == "__main__":
    application.debug = False
    application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    application.run()