#script to get trailer searches from google trends and dump to file
import ast
import time 
import pandas as pd
import numpy as np
import re, time
import warnings, requests
from bs4 import BeautifulSoup
import utils
from dateutil.parser import parse
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)

#metadata
df_full = pd.read_csv('data/movies_metadata.csv')

#function to get data from google trends
def google_trends_data(title):
    '''get trailer query data from google trends and '''
    import datetime
    import dateutil.relativedelta    
    print(title)
    query = title + ' ' + 'trailer'
    release_date = df_full[df_full.title == title].release_date.iloc[0]   
    end = datetime.datetime.strptime(release_date, "%Y-%m-%d") - dateutil.relativedelta.relativedelta(months=1)
    end = str(end.year) + '-' +  str(end.month) + '-' + str(end.day)
    start = datetime.datetime.strptime(end, "%Y-%m-%d") - dateutil.relativedelta.relativedelta(years=1)
    start = str(start.year) + '-' +  str(start.month) + '-' + str(start.day)
    
    kw_list = [query]
    pytrends.build_payload(kw_list, cat=0, timeframe=start + ' ' + end, geo='US', gprop='youtube')
    data_df = pytrends.interest_over_time().reset_index()

    if 'isPartial' in data_df.columns:
        data_df.drop('isPartial', axis = 1, inplace=True)    
    data_df.columns = ['dates', 'searches']
    return start, end, release_date, data_df

#code to write the data to file--------------------------------------------------------------

df2010US = pd.read_csv('data/data_since_2010.csv')
df2010US.drop('Unnamed: 0', axis =1, inplace=True)
titles = list(df2010US.title)

outf = open('data/searches_test', 'a')
outf.write('dates,searches,title\n')
for i, name in enumerate(titles):
    try:
        df = google_trends_data(name)[3]
        df['title'] = name
        df.to_csv(outf, header=False, index=False)
        time.sleep(6)
    except Exception as e:
        print(e, name, i)
