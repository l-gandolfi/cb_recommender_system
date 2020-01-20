import os.path as path
import pandas as pd
import numpy as np
import calendar
import datetime

#This file has been used to populate db with well formatted dates. 
#A temporaneous script has been used to populate the db. 
#Since it wasn't one of the main files it hasn't been put into the repository


#Creating a dict with year months mapped as ('Jan': 1) from Calendar
monthDict = dict((v,k) for k,v in enumerate(calendar.month_abbr))

#This is used to remove first element of monthDict that is a void key with no value ('': 0)
monthDict.pop('', None)

PATH =  path.abspath(path.join(__file__ ,"../.."))+'/tweets_data/'

df = pd.read_csv(PATH+'tweets_embedding.csv')

dates = df['date']

#Parsing dates
def date_parsing(dates):
    out = []
    for date in dates:
        #Normal dates
        if(type(date) is str):     
            #We have to type of dates, first ones well formatted
            if(date.startswith('20', 0, 3)):
                parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                out.append(parsed_date)
            #The others need to be cleaned
            else:
                splitted_date = date.split(" ")
                new_date = ''
                new_date += splitted_date[5]
                new_date += '-'
                new_date += str(monthDict[splitted_date[1]])
                new_date += '-'
                new_date += splitted_date[2]
                new_date += ' '
                new_date += splitted_date[3]
                parsed_date = datetime.datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S")
                out.append(parsed_date)
        #There are some broken dates       
        else:
            out.append(date)

    return out