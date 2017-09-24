import datetime
import pandas as pd
import numpy as np
from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify
from sklearn.neighbors import NearestNeighbors
import pickle
from search import *
from author import *

application = Flask(__name__)
p_loc, search_arr = pickle.load(file = open('./pickles/search_array.pickle', 'rb'))
user_id_map = pickle.load(file=open('./pickles/user_id_maps.pickle', 'rb'))
paper_dist =  pickle.load(file=open('./pickles/paper_dist_pruned.pickle', 'rb'))
nbr_auth = pickle.load(file=open('./pickles/nbr_auth.pickle', 'rb'))

@application.route('/')
def main():
    return render_template('index.html')

@application.route('/search/')
def search_decorator():
    query = request.args.get('term')
    return jsonify(autocomplete_search(query, search_arr, 0, 40))

@application.route('/paper/<query>')
def paper_decorator(query):
    cur_item =  search_arr[int(query) + p_loc]
    months = ["Unknown", "January", "Febuary", "March", "April", "May","June",
              "July", "August", "September", "October", "November", "December"]
    desc = ', '.join(cur_item[4])
    date = datetime.datetime.utcfromtimestamp(cur_item[5])
    desc = '(' + months[date.month] + ' '  + str(date.year) +') ' + desc
    if len(desc) > 70:
        desc = desc[:desc.find(', ',40)] + " and others"
    return render_template('paper.html', title = cur_item[0], subtitle = desc)

@application.route('/author/<query>')
def author_decorator(query):
    cur_item = search_arr[int(query)]
    subtitle = num_papers_sub(cur_item)
    distances, indices = nbr_auth.kneighbors(get_user_research(paper_dist, cur_item[3]))
    similar_authors = []
    for idx, i in enumerate(indices[0]):
        if idx > 0:
            similar_authors.append((search_arr[i, 0], num_papers_sub(search_arr[i, :]), "/author/" + str(search_arr[i, 2])))
    author_papers = get_papers_list(cur_item, int(query), search_arr, p_loc)
    print(author_papers)
    return render_template('author.html', title = cur_item[0].title(), subtitle= subtitle, similar = similar_authors, papers = author_papers)

# run the application.
if __name__ == "__main__":
    application.debug = False
    application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    application.run()