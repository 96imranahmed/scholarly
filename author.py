import numpy as np
import datetime as datetime 

def get_user_research(paper_topic_dist, paper_indxs):
    user = np.zeros(np.shape(paper_topic_dist)[1])
    for idx in paper_indxs:
        user = np.add(user, paper_topic_dist[idx, :])
    return user.reshape(1, -1)

def num_papers_sub(row):
    subtitle = " paper"
    if len(row[3]) > 1:
        subtitle = str(len(row[3])) + subtitle + 's'
    else:
        subtitle = 'One' + subtitle
    return subtitle

def get_papers_list(row, author_id, search_arr, paper_offset):
    papers = row[3]
    paper_names = [i.replace("\n", "").replace("  ", " ") for i in row[4]]
    paper_dates = []
    paper_dates_text = []
    co_authors = []
    months = ["Unknown", "January", "Febuary", "March", "April", "May","June",
                      "July", "August", "September", "October", "November", "December"]   
    for paper in papers:
        raw = search_arr[paper_offset + paper, :]
        date = datetime.datetime.utcfromtimestamp(raw[5])
        desc = '(' + months[date.month] + ' '  + str(date.year) +')'
        paper_dates_text.append(desc)
        paper_dates.append(raw[5])
        paper_co_auth = ', '.join(raw[4])
        if len(paper_co_auth) > 70:
            paper_co_auth = paper_co_auth[:paper_co_auth.find(', ',40)] + " and others"
        co_authors.append(paper_co_auth)
    papers = ['/paper/' + str(item) for item in papers]
    zipper = list(zip(papers, paper_names, paper_dates_text, co_authors, paper_dates))
    zipper = sorted(zipper, key=lambda k: k[-1], reverse= True)
    return zipper