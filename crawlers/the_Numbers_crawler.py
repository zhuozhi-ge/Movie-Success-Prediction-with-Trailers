#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import pandas as pd


# In[80]:


# get all the movies from 2009 to 2019
data_1 = {
    "title": [],
    "genre": [],
    "url": [],
    "revenue_to_data": [],
}
head = "https://www.the-numbers.com"
years = range(2009, 2020)
for year in years:
    req = requests.get('https://www.the-numbers.com/movies/year/{}'.format(year))
    webpage = req.text
    with open("data/movies_year_{}.text".format(year), "w", encoding='utf-8') as f:
        f.write(webpage)
    soup = BeautifulSoup(webpage)
    trs = soup.find("table").find_all("tr")[2:]
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) == 6 and tds[3].text == 'Theatrical':
            url = head + tds[1].find("a")["href"]
            data_1["title"].append(tds[1].text)
            data_1["genre"].append(tds[2].text)
            data_1["revenue_to_data"].append(float(tds[4].text.strip("$").replace(",","")))
            data_1["url"].append(url)


# In[80]:


# get all the movies from 2009 to 2019
data_1 = {
    "title": [],
    "release_date": [],
    "genre": [],
    "url": [],
    "revenue_to_data": [],
}
head = "https://www.the-numbers.com"
years = range(2009, 2020)
DATE = ""
for year in years:
    req = requests.get('https://www.the-numbers.com/movies/year/{}'.format(year))
    webpage = req.text
#     with open("data/movies_year_{}.text".format(year), "w", encoding='utf-8') as f:
#         f.write(webpage)
    soup = BeautifulSoup(webpage)
    trs = soup.find("table").find_all("tr")[2:]
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) == 6 and tds[3].text == 'Theatrical':
            date = tds[1].text
            if date:
                DATE = date
            data_1["release_date"].append(DATE)    
            url = head + tds[1].find("a")["href"]
            data_1["title"].append(tds[1].text)
            data_1["genre"].append(tds[2].text)
            data_1["revenue_to_data"].append(float(tds[4].text.strip("$").replace(",","")))
            data_1["url"].append(url)


# In[82]:


movies_list_df = pd.DataFrame(data_1)
movies_list_df.head()
print(movies_list_df.shape)


# In[83]:


movies_list_df.to_csv("data/movies_list.csv")


# In[98]:


# helper functions to get opening revenue, budget and theater counts
def get_budget(webpage):
    target_pos_tag = webpage.find("Production&nbsp;Budget:")
    if target_pos_tag != -1:
        target_pos_start = webpage.find("<td>", target_pos_tag)
        target_pos_end = webpage.find("</td>", target_pos_start)
        target = webpage[target_pos_start + 5 : target_pos_end]
        target = target[:target.find(" ")]
        target = float(target.replace(",", ""))
        return target

def open_theaters(webpage):
    target_pos_tag = webpage.find("Theater counts:")
    if target_pos_tag != -1:
        target_pos_start = webpage.find("<td>", target_pos_tag)
        target_pos_end = webpage.find("</td>", target_pos_start)
        target = webpage[target_pos_start + 4 : target_pos_end]
        target = target[:target.find(" ")]
        target = float(target.replace(",", ""))
        return target

def open_wk(webpage):
    target_pos_tag = webpage.find("Opening&nbsp;Weekend:")
    if target_pos_tag != -1:
        target_pos_start = webpage.find("<td>", target_pos_tag)
        target_pos_end = webpage.find("</td>", target_pos_start)
        target = webpage[target_pos_start + 5 : target_pos_end]
        target = target[:target.find(" ")]
        target = float(target.replace(",", ""))
        return target                        
                                  
def get_run_time(webpage):
    target_pos_tag = webpage.find("Running Time:")
    if target_pos_tag != -1:
        target_pos_start = webpage.find("<td>", target_pos_tag)
        target_pos_end = webpage.find("</td>", target_pos_start)
        target = webpage[target_pos_start + 4 : target_pos_end]
        target = target[:target.find(" ")]
        target = float(target)
        return target


# In[ ]:


# get detailed movie information with opening revenue and budget
data_2 = {
    "title": [],
    "weekend_rev": [],
    "theater_count": [],
    "weekend_rev_mean": [],
    "budget": [],
    "run_time": [],
}
for title, url in zip(movies_list_df["title"], movies_list_df["url"]):
    try:
        for i in range(3):
            time.sleep(i)
        webpage = requests.get(url).text
        weekend_rev = open_wk(webpage)
        theater_count = open_theaters(webpage)
        budget = get_budget(webpage)
        run_time = get_run_time(webpage)
        if weekend_rev and theater_count and budget and run_time > 60:
            data_2["title"].append(title)
            data_2["budget"].append(budget)
            data_2["weekend_rev"].append(weekend_rev)
            data_2["theater_count"].append(theater_count)
            data_2["weekend_rev_mean"].append(weekend_rev / theater_count)
            data_2["run_time"].append(run_time)
    except:
        print("scraping interrupted")
        time.sleep(60)
        print("scraping restarted")
        pass
        


# In[109]:


url = "https://www.the-numbers.com/movie/Little-Fockers#tab=summary"
webpage = requests.get(url).text
soup = BeautifulSoup(webpage)
soup


# In[114]:


movies_finance_df = pd.DataFrame(data_2)
movies_finance_df.head()
print(movies_finance_df.shape)

