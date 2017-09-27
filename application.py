import datetime
import pandas as pd
import numpy as np
from flask import Flask, abort, flash, redirect, render_template, request, url_for, jsonify
from sklearn.neighbors import NearestNeighbors
import pickle
from search import *
from author import *
from paper import *
import random

application = Flask(__name__)
p_loc, search_arr = pickle.load(file = open('./pickles/search_array.pickle', 'rb'))
user_id_map = pickle.load(file=open('./pickles/user_id_maps.pickle', 'rb'))
paper_dist =  pickle.load(file=open('./pickles/paper_dist_pruned.pickle', 'rb'))
nbr_auth = pickle.load(file=open('./pickles/nbr_auth.pickle', 'rb'))
nbr_paper = pickle.load(file=open('./pickles/nbr_paper.pickle', 'rb'))

@application.route('/')
def main():
    return render_template('index.html')

@application.route('/search/')
def search_decorator():
    query = request.args.get('term')
    return jsonify(autocomplete_search(query, search_arr, 0, 40))

@application.route('/paper/<query>')
def paper_decorator(query):
    cur_item = search_arr[int(query) + p_loc]
    details =  get_paper_details(cur_item)
    authors = []
    for idx, auth_id in enumerate(cur_item[3]):
        rdm_paper = str(random.choice(search_arr[auth_id, 4]))
        authors.append((cur_item[4][idx].title(), num_papers_sub(search_arr[auth_id, :]), "/author/" + str(auth_id), rdm_paper.replace("\n", "").replace("  ", " ")))
    distances, indices = nbr_paper.kneighbors(paper_dist[int(query)].reshape(1, -1)) 
    similar_papers = []
    for idx, i in enumerate(indices[0]):
        if not i == int(query):
            sim_p =  search_arr[int(i) + p_loc]
            entry = list(get_paper_details(sim_p))
            entry.append(str(round(distances[0][idx], 3)))
            similar_papers.append(entry)
    similar_papers = similar_papers[:10]
    return render_template('paper.html', title = details[1], subtitle = details[2], authors = authors, similar_papers = similar_papers)

@application.route('/author/<query>')
def author_decorator(query):
    cur_item = search_arr[int(query)]
    subtitle = num_papers_sub(cur_item)
    distances, indices = nbr_auth.kneighbors(get_user_research(paper_dist, cur_item[3]))
    similar_authors = []
    for idx, i in enumerate(indices[0]):
        if not i == int(query):
            rdm_paper = str(random.choice(search_arr[i, 4]))
            similar_authors.append((search_arr[i, 0].title(), num_papers_sub(search_arr[i, :]), "/author/" + str(search_arr[i, 2]), rdm_paper.replace("\n", "").replace("  ", " "), str(round(distances[0][idx], 3))))
    similar_authors = similar_authors[:10]
    author_papers = get_papers_list(cur_item, int(query), search_arr, p_loc)
    return render_template('author.html', title = cur_item[0].title(), subtitle= subtitle, similar = similar_authors, papers = author_papers)

# run the application.
if __name__ == "__main__":
    application.debug = False
    application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    application.run()