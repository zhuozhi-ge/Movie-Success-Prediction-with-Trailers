#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from utils import get_movie_info


# In[2]:


id_df = pd.read_json('movie_ids_10_25_2020.json', lines=True)


# In[3]:


id_df.head()


# In[4]:


data = {
    "id": [],
    "title": [],
    "budget": [],
    "revenue": [],
    "genres": [],
    "production_companies": [],
    "production_countries": [],
    "release_date": [],
    "runtime": []
}
c = 0
for m_id in id_df["id"][-10000:]:
    try:
        info = get_movie_info(m_id)
        if info["budget"] > 0:
            c += 1
            print(c)
            for key in data.keys():
                data[key].append(info[key])
    except:
        pass
    if c > 99:
        break
# for m_id in id_df["id"]:
#     try:
#         info = get_movie_info(m_id)
#         if "2010" < info["release_date"] < "2020" and info["budget"] > 0:
#             for key in data.keys():
#                 data[key].append(info[key])
#     except:
#         pass


# In[5]:


temp_df = pd.DataFrame(data)
temp_df.shape


# In[7]:


temp_df.to_csv("./data/movies_metadata.csv")

