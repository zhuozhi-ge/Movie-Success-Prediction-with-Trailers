#script to preprocess full data
import ast
import pandas as pd
import numpy as np
import re, time
import warnings, requests
from bs4 import BeautifulSoup
import datetime
import utils
from dateutil.parser import parse
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)


#define some functions

def get_month(x):
    '''helper function to get release month'''
    try:
        return month_order[x.month-1]
    except:
        return np.nan
    
def get_day(x):
    '''helper function to get release day'''
    try:
        return day_order[x.weekday()]
    except:
        return np.nan


def get_max_date(title):
    '''return date of the trailer with most online searches'''
    return peaks_series.loc[title].loc[peaks_series.loc[title]['peak_values'].idxmax()][0]

def get_second_max_date(title):
    if len(peaks_series.loc[title])>1:       
        df = peaks_series.loc[title][peaks_series.loc[title].peak_values != 100]
        return df.loc[df['peak_values'].idxmax()][0]
    else: return 0
    
def get_release_date(title):
    '''helper function to get release date'''
    return pd.to_datetime(df_final.loc[title].release_date)

def dt_main(title):
    '''return the number of days between largest trailer peak and release date'''
    return (get_release_date(title) - pd.to_datetime(get_max_date(title))).days
    
def dt_trailers(title):
    '''return the number of days between the two largest peak trailers'''
    from dateutil import relativedelta
    if get_second_max_date(title) == 0:
        return 0
    else:
        return (get_max_date(title) - get_second_max_date(title)).days

def get_movie(title):
    '''helper function to get movie title'''
    return searches.loc[searches.title==title]['searches'].copy()

def views_proxy(title):  
    '''estimate views prior to release date using views today'''
    release_date = get_release_date(title)
    if get_second_max_date(title)!=0:
        start = min(get_max_date(title), get_second_max_date(title))
    else: 
        start = get_max_date(title)
    delta_t1 = (pd.to_datetime(datetime.datetime.today())- start).days
    delta_t2 = (release_date - start).days
    tot_views = df[df.title == title].views.iloc[0]
    views_proxy = (tot_views/delta_t1)*(delta_t2)
    return np.round(views_proxy)

def like_score(df):
    return df_final['views']*df_final['likes']/(df_final['likes'] + df_final['dislikes'])

def like_score_proxy(df):
    return df_final['views_proxy']*df_final['likes']/(df_final['likes'] + df_final['dislikes'])

def categorize(s):
    '''function to make dt_trailers categorical '''
    res =[]
    for v in s:
        if v==0:
            res.append('zero')
        elif v>0:
            res.append('pos')
        else: 
            res.append('neg')
    return res 

def get_peaks(x,thres, min_dist):
    '''return the indices of the top peaks and their values in the google trends.
        to be uses when perfoming groupby below'''
    import peakutils
    data = x.values
    baseline_values = peakutils.baseline(data)
    data_without_baseline = data - baseline_values
    peakind = peakutils.indexes(data_without_baseline, thres=thres, min_dist=min_dist)
    dates = x.index
    dates_series = pd.Series(dates)
    data_df = pd.DataFrame(data)
    #peak_values = list(data_df.loc[peakind].values)
    peak_dates = dates_series[peakind]
    peak_values = data[peakind]
    
    return pd.DataFrame({'peak_dates':peak_dates, 'peak_values':peak_values})

#get data and preprocess----------------------------------------------------

#get metadata from the Movie Database
df_full = pd.read_csv('data/movies_metadata.csv')

#fix some errors in data
df_full.budget[df_full.title=='Dope'] = 7000000
df_full.budget[df_full.title=='The Letters'] = 20000000

#here is a dict to quickly get ids from movie titles and vice versa
title2id = {k:v for k, v in zip(df_full['title'], df_full['id'])}
id2title = {k:v for k, v in zip(df_full['id'], df_full['title'])}

# get openening weekend info scraped from the Box Office Mojo
weekend_df = pd.read_csv('data/opening_weekend_data.csv')
weekend_df.columns = ['title', 'weekend_rev', 'weekend_rev_mean']
weekend_df['num_theaters']= np.round(weekend_df['weekend_rev']/weekend_df['weekend_rev_mean'])

#merge data sets
df = df_full.set_index('title').join(weekend_df.set_index('title'), how='inner').drop_duplicates().reset_index()

#preprocess data
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
df = df[df.budget >1000000]

df.drop(['adult', 'id', 'imdb_id', 'belongs_to_collection', 'homepage', 'original_title', 
               'poster_path', 'popularity', 'vote_average', 'vote_count', 'spoken_languages',
               'status', 'video', 'revenue', 'tagline', 'overview'], axis=1, inplace=True)

df['success'] = df['weekend_rev'] / df['budget']
df = df[~df['success'].isnull()].copy()
df = df[~df['release_date'].isnull()].copy()
df['release_date'] = df['release_date'].apply(parse)


month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def get_month(x):
    try:
        return month_order[x.month-1]
    except:
        return np.nan
    
def get_day(x):
    try:
        return day_order[x.weekday()]
    except:
        return np.nan

df['day'] = df['release_date'].apply(get_day)
df['month'] = df['release_date'].apply(get_month)
df['holiday'] = df['month'].apply(
    lambda x: 'Yes' if x in ['Jan', 'Feb', 'May', 'July', 'Sep', 'Oct', 'Nov', 'Dec'] else 'No')
df['year'] = df['release_date'].apply(lambda x: x.year)

df['log_budget']= df['budget'].apply(np.log10)
df['log_weekend_rev']= df['weekend_rev'].apply(np.log10)
df['log_weekend_rev_mean']= df['weekend_rev_mean'].apply(np.log10)

#only include movies released in or after 2010
df2010 = df[df['year']>=2010].copy()
df2010.drop_duplicates(inplace=True)

#drop error-prone movies
df2010 = df2010[df2010.title != 'Camille Claudel 1915']
df2010 = df2010[df2010.title != 'Instructions Not Included']
df2010 = df2010[df2010.title != 'In Order of Disappearance trailer']
df2010.reset_index(inplace=True, drop=True)

#use ast.literal_eval to convert stringified dicts into usable dicts
df2010['production_countries'] = df2010['production_countries'].fillna('[]').apply(ast.literal_eval)
df2010['production_countries'] = df2010['production_countries'].apply(
    lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

#only keep movies if the US is in the list of production countries 
index_US = []
for i in list(df2010.index):
    if 'United States of America' in df2010['production_countries'].iloc[i]:
        index_US.append(i)        
df2010US = df2010.iloc[index_US].reset_index(drop=True)

# get youtube trailer data
youtube_trailers = pd.read_csv('data/youtube_trailers.csv')

#merge with df2010US
df_merged = df2010US.merge(youtube_trailers, how='inner')
df_merged.to_csv('data/data_since_2010.csv')

#get movie data for movies released >= 2010 and with production countries always including the US.
del df
df = pd.read_csv('data/data_since_2010.csv')
df.drop('Unnamed: 0', axis =1, inplace=True)

# import data 
searches = pd.read_csv('data/searches') #first take
searches2010 = pd.read_csv('searches2010')[1:] #second take
searches = pd.concat([searches2010, searches]).drop_duplicates()

#uncomment these if you want search data per month (rather than per week)
#searches2010_monthly = pd.read_csv('searches2010_monthly')
#searches2010_monthly.drop_duplicates(inplace=True)
#searches2010_monthly.set_index('dates', inplace = True)
#searches_total_volume = searches2010_monthly.groupby('title').searches.apply(sum)
#searches2010_monthly.searches = searches2010_monthly.searches.astype(int)


#clean up dataframe a bit
searches.set_index('dates', inplace = True)
searches.drop('dates', inplace = True)
searches.reset_index(inplace=True)
searches.drop_duplicates(inplace=True)
searches.set_index('dates', inplace = True)
searches.index =pd.DataFrame(searches.index).apply(lambda x: pd.to_datetime(x, format='%Y/%m/%d')).dates
searches.searches = searches.searches.astype(int)

# find the peak index location for each peak
g = searches.groupby('title')
peaks_series = g['searches'].apply(lambda x: get_peaks(x, thres=0.20, min_dist=8))
search_volume = g['searches'].apply(sum)
search_mean = g['searches'].apply(np.mean)

num_peaks =[]
for m in list(search_volume.index):
    n=len(peaks_series.loc[m])
    num_peaks.append(n)

df_trends = pd.DataFrame({'search_volume':search_volume, 'search_mean':search_mean, 'num_peaks':num_peaks})

#merge all data frames together
df_final = df_trends.join(df.set_index('title'), how = 'inner')

df_final = df_final[df_final.index!='No One Lives']
df_final = df_final[df_final.num_peaks != 0]

#days from the largest peak to release day
dt_main_list = []
for title in list(df_final.index):
    #print(title)
    try:
        dt_m = dt_main(title)
    except: 
        dt_m =0
    dt_main_list.append(dt_m)
    
#days from the largest peak to release day
dt_trailers_list = []
for title in list(df_final.index):
    #print(title)
    dt_t = dt_trailers(title)
    dt_trailers_list.append(dt_t)
    
#views proxy
views_proxy_list =[]
for title in list(df_final.index):
    #print(title)
    v = views_proxy(title)
    views_proxy_list.append(v)
    
df_final['dt_main'] = dt_main_list
df_final['dt_trailers'] = dt_trailers_list
df_final['dt_trailers_cat'] = categorize(df_final['dt_trailers'])

df_final['views_proxy'] = views_proxy_list
#df_final['like_score'] = like_score(df_final)
#df_final['like_score_proxy'] = like_score_proxy(df_final)

#log values today
df_final['log_views'] = df_final['views'].apply(np.log10)
#df_final['log_like_score'] = df_final['like_score'].apply(np.log10)
#df_final['log_search_mean'] = df_final['search_mean'].apply(np.log10)
df_final['log_search_volume'] = df_final['search_volume'].apply(np.log10)

#proxies with scaled values between trailer release and movie release
df_final['log_views_proxy'] = df_final['views_proxy'].apply(np.log10)
#df_final['log_like_score_proxy'] = np.log(like_score_proxy(df))
df_final = df_final[(df_final['dt_main']<500)&(df_final['dt_main']!=0)]
#df_final.drop(['views', 'like_score', 'search_mean', 'search_volume'], axis=1)

df_final.to_csv('data/df_final.csv')