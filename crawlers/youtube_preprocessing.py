#script to preprocess the youtube trailer data output from youtube_scraper.py

#get Youtube trailer data (release date, views, likes, dislikes)
import pandas as pd
import numpy as np
import pickle

#get metadata from the Movie Database
df_full = pd.read_csv('data/movies_metadata.csv')

#here is a dict to quickly get titles from movie ids
id2title = {k:v for k, v in zip(df_full['id'], df_full['title'])}

#get youtube trailer data 
with open ('data/youtube_data', 'rb') as fp:
    trailersData = pickle.load(fp)
        
trailers = pd.Series(trailersData)

trailers_df = pd.DataFrame({'trailers':trailers})

#get index of df without empty lists
trs=[]
for t in trailers_df.trailers:
    if len(t)==0:
        t = np.nan
    trs.append(t)
    del t
trs = pd.Series(trs)
trs.dropna(how='any', inplace=True)
idx = list(trs.index)

trailers_df = trailers_df.iloc[idx]

# create list that includes all trailers
trailers_series = trailers_df.apply(lambda x: pd.Series(x['trailers']),axis=1).stack().reset_index(level=1, drop=True)
trailers_series.name = 'trailers'
trailers_series.reset_index(drop=True, inplace=True)

#collect all trailer info into a convenient data frame with each movie as row
dislikes = []
likes = []
ids = []
name = []
youtube_date = []
Type = []
views = []
for i in range(len(trailers_series)):
    d = trailers_series.iloc[i].get('dislikes', '-1')
    l = trailers_series.iloc[i].get('likes', '-1')
    movieid = trailers_series.iloc[i].get('movieid','-1')
    n = trailers_series.iloc[i].get('name', '-1')
    p = trailers_series.iloc[i].get('publication_date', '-1')
    T = trailers_series.iloc[i].get('type', '-1')
    v = trailers_series.iloc[i].get('views', '-1')
    dislikes.append(d)
    likes.append(l)
    ids.append(movieid)
    name.append(n)
    youtube_date.append(p)
    Type.append(T)
    views.append(v)
    
views = pd.Series(views)
ids = pd.Series(ids)
trailers_cat = pd.DataFrame({'ids':ids, 'name':name,'type':Type, 'youtube_date':youtube_date})
trailers_num = pd.DataFrame({'ids':ids,'dislikes':dislikes, 'likes':likes, 'views':views })

#drop some rows and columns
trailers_num = trailers_num.set_index('dislikes').drop('-1').reset_index()
trailers_num = trailers_num.set_index('likes').drop('-1').reset_index()
trailers_num = trailers_num.set_index('views').drop('-1').reset_index()
trailers_num = trailers_num.set_index('ids').drop('-1').reset_index()

trailers_cat = trailers_cat.set_index('ids').drop('-1').reset_index()
trailers_cat = trailers_cat.set_index('name').drop('-1').reset_index()
trailers_cat = trailers_cat.set_index('type').drop('-1').reset_index()
trailers_cat = trailers_cat.set_index('youtube_date').drop('-1').reset_index()

trailers_num['title'] = trailers_num['ids'].apply(lambda x: id2title[x])
trailers_cat['title'] = trailers_cat['ids'].apply(lambda x: id2title[x])
trailers_num.drop('ids', axis=1, inplace = True)
trailers_cat.drop('ids', axis=1, inplace = True)

#clean up a bit and change to numeric
trailers_num['dislikes'] = trailers_num['dislikes'].apply(lambda x: x.replace(',',''))
trailers_num['likes'] = trailers_num['likes'].apply(lambda x: x.replace(',',''))
trailers_num['views'] = trailers_num['views'].apply(lambda x: x.replace(',',''))

trailers_num['dislikes'] = pd.to_numeric(trailers_num['dislikes'])
trailers_num['likes'] = pd.to_numeric(trailers_num['likes'])
trailers_num['views'] = pd.to_numeric(trailers_num['views'])

youtube_trailers = np.round(trailers_num.groupby('title').mean().dropna())
youtube_trailers.to_csv('data/youtube_trailers.csv')
