import numpy as np
import random
import datetime

def autocomplete_search(term, matrix, search_indx, limit = 100):
    op = {}
    op_papers = []
    term = term.strip()
    term_min = 3
    show_paper = True
    show_author = True
    filter_surname = False
    sn_chk = "?surname="
    paper_chk = "?paper"
    author_chk = "?author"
    surname = ""
    if paper_chk in term:
        show_author = False
        term = term.replace(paper_chk, '').strip()
    if sn_chk in term and ';' in term:
        surname = term.lower()[term.find(sn_chk)+len(sn_chk):term.find(';', term.find(sn_chk))].strip()
        term = term.replace(term[term.find(sn_chk):term.find(';', term.find(sn_chk))+1], "").strip()
        filter_surname = True
    if author_chk in term:
        show_paper = False
        term = term.replace(author_chk, '').strip()
    if len(term) < term_min and not filter_surname: 
        return {}
    for idx, val in np.ndenumerate(matrix[:, search_indx]):
        row = matrix[idx, :]
        val = val.replace("\n", "").replace("  ", " ")
        if len(term) >= term_min and (term in val or term.lower() in val.lower()):
            row[0][search_indx] = val.strip()
            if row[0][1] == 'author' and show_author:
                if filter_surname:
                    if surname.lower() in val.split()[-1].lower():
                        op[int(np.squeeze(idx))] = row
                else:
                    op[int(np.squeeze(idx))] = row
            elif row[0][1] == 'paper' and show_paper:
                if filter_surname:
                    for auth in row[0][4]:
                        if surname.lower() in auth.split()[-1].lower():
                            op_papers.append((int(np.squeeze(idx)), row))
                            break
                else:
                    op_papers.append((int(np.squeeze(idx)), row))
        elif row[0][1] == 'paper' and filter_surname and len(term.strip()) == 0:
                for auth in row[0][4]:
                    if surname in auth.split()[-1].lower():
                        op_papers.append((int(np.squeeze(idx)), row))
                        break
        if len(op.keys()) + len(op_papers) > limit:
            break
    if len(op_papers) + len(op.keys()) == 0:
        return []
    results = {"results":{"category1":{"name":"Authors", "results":[]}, "category2":{"name": "Papers", "results":[]}}}
    for op_key in op:
        in_data = op[op_key][0]
        desc = in_data[4]
        title = in_data[0]
        url = ""
        if in_data[1] == 'author':
            title = title.title()
            desc = str(len(in_data[3])) + " paper(s) including: '" + random.choice(in_data[4]).replace("\n", "").replace("  ", " ").strip() + "'"
            url = "/author/" + str(in_data[2])
            entry = {"title":title, "description":desc, "url":url}
            results['results']['category1']['results'].append(entry)
        else: 
            pass
    #Sort list of papers
    op_papers = sorted(op_papers, key=lambda k: k[1][0][5], reverse= True)
    for paper in op_papers:
        in_data = paper[1][0]
        desc = in_data[4]
        title = in_data[0].replace("\n", "").replace("  ", " ")
        if in_data[1] == 'paper':
            months = ["Unknown", "January", "Febuary", "March", "April", "May","June",
                      "July", "August", "September", "October", "November", "December"]
            date = datetime.datetime.utcfromtimestamp(in_data[5])
            desc = ', '.join(desc)
            desc = '(' + months[date.month] + ' '  + str(date.year) +') ' + desc
            url = "/paper/" + str(in_data[2])
            if len(desc) > 70:
                desc = desc[:desc.find(', ',40)] + " and others"
            entry = {"title":title, "description":desc, "url":url}
            results['results']['category2']['results'].append(entry)
    return results