#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, r2_score
from xgboost import XGBRegressor

np.random.seed(42)


# In[2]:


df = pd.read_csv('df_movies.csv')


# In[3]:


df['log_views'] = df[df.views!=0].views.apply(np.log)
df['log_likes'] = df[df.likes!=0].likes.apply(np.log)
df['log_dislikes'] = df[df.dislikes!=0].dislikes.apply(np.log)
date = pd.to_datetime(df["release_date"])
df["weekday"] = date.dt.weekday
df["month"] = date.dt.month
df['log_budget']= df['budget'].apply(np.log10)

# one-hot encoding genres
df["genres"] = df["genres"].apply(lambda x: x.strip("[").strip("]").replace("'","").replace(" ","").split(","))
s = df.apply(lambda x: pd.Series(x['genres']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'genre'
gen_df = df.drop('genres', axis=1).join(s)
pop_gen = pd.DataFrame(gen_df['genre'].value_counts()).reset_index()
pop_gen.columns = ['genre', 'movies']
for genre in pop_gen["genre"]:
    df["g_" + genre] = 0
    for idx in range(len(df)):
        if genre in df["genres"][idx]:
            df["g_" + genre][idx] = 1
            
# apply constrains to get rid of outliers
df = df[df.success<=3]
df = df[df.budget>=10000000]
df = df[df.runtime>80]

df.eval('view_score = views*(likes - dislikes)/(likes + dislikes)*search_volume', 
        inplace=True)
df["view_score"] = df["view_score"].apply(np.log)

df = df.drop(['title', 'genres', 'production_companies', 'production_countries', 
              'release_date', 'views', 'likes', 'dislikes', 'budget'], axis=1)
df = df.dropna()


# In[4]:


# Creat train and test data sets
X, y = df.drop('success', axis=1), df['success'].copy()

# Gridserach to find the best hyper parameters

params = {
     "xgb__n_estimators": [100, 300],
     "xgb__reg_alpha": range(5, 20)[::2],
     "xgb__reg_lambda": range(50, 201)[::10]
}


steps = [("scale", RobustScaler()),
         ("xgb", XGBRegressor(random_state=42, objective='reg:squarederror'))]

model = Pipeline(steps)

scorer = make_scorer(r2_score)

clf = GridSearchCV(model, params, scoring=scorer)

clf.fit(X, y)

model = clf.best_estimator_

model.fit(X, y)
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)


# In[ ]:




