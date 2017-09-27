import numpy as np
import datetime as datetime

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