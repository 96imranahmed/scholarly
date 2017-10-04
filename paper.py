import numpy as np
import datetime as datetime
import difflib
import re, string

def get_paper_details(cur_item):
    months = ["Unknown", "January", "Febuary", "March", "April", "May","June",
              "July", "August", "September", "October", "November", "December"]
    desc = ', '.join(cur_item[4])
    date = datetime.datetime.utcfromtimestamp(cur_item[5])
    desc = '(' + months[date.month] + ' '  + str(date.year) +') ' + desc
    if len(desc) > 70:
        desc = desc[:desc.find(', ',40)] + " and others"
    title = cur_item[0].replace("\n", "").replace("  ", " ")
    url = '/paper/' + str(cur_item[2])
    return (url, title, desc)

def gen_word_cloud(dist,topics, num_required = 5):
    items = []
    pattern = re.compile('[\W_]+')
    #Presort list
    dist = [(round(conf, 3), idx) for idx, conf in enumerate(list(dist)) if not ((np.isnan(conf)) or (conf < 0))]
    dist = sorted(dist, key = lambda p: p[0], reverse = True)
    for val in dist:
        if len(items) < num_required and not 'al.' in topics[val[1]]:
            items.append([val[0], topics[val[1]]])
    for item in items:
        item[1] = [pattern.sub('', i) for i in item[1] if len(i) > 2]
        pure_lst = []
        removables = set()
        for i in range(len(item[1])):
            if item[1][i] not in removables:
                matches = difflib.get_close_matches(item[1][i], item[1], n=5, cutoff=0.6)
                pure_lst.append(matches[0])
                removables.update(matches)
        item[1] = ', '.join([i.title() for i in pure_lst])
    return items