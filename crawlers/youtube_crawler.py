#scrape youtube for trailer metadata (release date, views, likes, dislikes) and dump to file
from bs4 import BeautifulSoup
import re, requests, time
from utils import get_movie_info, get_url
import pickle
import pandas as pd

def get_soup(url):
    """open url and return BeautifulSoup object, or None if site does not exist"""
    result = requests.get(url)
    if result.status_code != 200: return None
    time.sleep(0.01) # slow down as per youtube 'terms of use' to human speed
    return BeautifulSoup(result.text, 'html.parser')

def get_youtube_video_info(url, id):
    """ scrape youtube to get video info get video info"""
    soup = get_soup(url) #get video page and pull information from it 
    d = {} # collect video info in dict
    counter = 0
    #print(type(soup))
    
    if soup is None:
        return None

    #get views
    viewsfind = soup.find('div', class_='watch-view-count')
    if viewsfind is None:
        print('Finding watch-view-count failed. The movie id is {}'.format(id))
    else:
        views= viewsfind.text
        d['views'] = ''.join(c for c in views if c in "0123456789")
    
    #get publication date
    pubdate = soup.find('strong', class_="watch-time-text")
    if pubdate is None:
        print('Finding watch-time-text failed. The movie id is {}'.format(id))
    else:
        d['publication_date'] = pubdate.text[len('Published on ')-1:]
    
    #get likes
    likebutton = soup.find('button', class_="like-button-renderer-like-button")
    if likebutton is None:
        print('Finding renderer-like failed. The movie id is {}'.format(id))
    else:
        o = likebutton.find('span',class_ = 'yt-uix-button-content')
        d['likes'] = o.text if o else ""
   
    #get dislikes
    disbutton = soup.find('button', class_="like-button-renderer-dislike-button")
    if disbutton is None:
        print('Finding renderer-dislike failed. The movie id is {}'.format(id))
    else:
        o = disbutton.find('span',class_ = 'yt-uix-button-content')
        d['dislikes'] = o.text if o else ""

    print("finished processing movie {}".format(id))
    return d

def add_trailer_info(id):
    '''scrape Youtube to append trailer info to the output of get_movie_info(id).'''
    movieInfo = get_movie_info(id)
    trailers = get_url(id)
    
    for i in range(len(trailers)):
        url = trailers[i]
        trailer_dic = get_youtube_video_info(url, id)
        if trailer_dic is None or trailer_dic=={}:
            print('Did not work. The movie id is {} and trailer index is {}'.format(id, i))
            break
            
        dislikes = trailer_dic['dislikes']
        movieInfo['trailers']['youtube'][i].update({'dislikes':dislikes})

        likes = trailer_dic['likes']
        movieInfo['trailers']['youtube'][i].update({'likes':likes})

        publication_date = trailer_dic['publication_date']
        movieInfo['trailers']['youtube'][i].update({'publication_date':publication_date})

        if trailer_dic == {}: break
        views = trailer_dic['views']
        movieInfo['trailers']['youtube'][i].update({'views':views})
        
        movieInfo['trailers']['youtube'][i].update({'movieid':id})        
    return movieInfo

#scrape youtube and get trailer data
ids = list(pd.read_csv('data/movies_metadata.csv').id)
trailer_info = []
counter =0
for i in ids:
    try:
        a = add_trailer_info(i)['trailers']['youtube']
    except Exception as e:
        print('Exception is {}'.format(e))
        continue
    print('counter = {}'.format(counter))
    counter = counter + 1
    trailer_info.append(a)

with open ('data/youtube_data', 'wb') as fp:
    pickle.dump(trailer_info, fp)
    
#def scrape_youtube_data(ids):
#    import time
#    import csv
#    df_full = pd.read_csv('data/movies_metadata.csv')
#    id2title = {k:v for k, v in zip(df_full['id'], df_full['title'])}
    
#    outf = open('data/youtube_data.csv', 'a')
#    writer = csv.writer(outf)
#    outf.write('title, trailers\n')
#    with outf:
#        for i, ID in enumerate(ids):
#            try:
#                trailers = add_trailer_info(i)['trailers']['youtube']
#                if trailers!=[]:
#                    writer.writerow([id2title[ID], trailers])
#                    print('{}: scraping youtube trailer info for {}'.format(i, id2title[ID]))
#                    #time.sleep(1)
#            except Exception as e:
#                print(e, id2title[ID], i)
            
#df_full = pd.read_csv('data/movies_metadata.csv')
#ids = df_full.id

#scrape_youtube_data(ids)
