# Movie-Success-Prediction-with-Trailers
**Problem statement**
<br>The success of a movie can be predicated using social media analytics. The audience expectations and movie buzz can be measured from the data gathered via social media platforms. Video-sharing websites like YouTube encourages interaction among its users through the provision of user reviewing facility of movie trailers. In this project, I gather data about movie trailers by scraping the internet and using API's from different sources. I then build a model that uses this dataset (things like online search trends prior to release date, etc) to predict the initial success of a movie.

**Features**
1. title: movie's title.
2. genres: movie's genres.
3. production_companies: movie's list of production companies.
4. production_countries: movie's list of production countires.
5. release_date: movie's release data.
6. runtime: movie duration in minutes (we restrict to movies with at least 80 minutes long).
7. budget: movie's budget (excluding marketing costs, which are typically as large as the budget itself).
8. num_peaks: number of online search peaks from Google Trends corresponding to a movie trailer. 
9. search_volume: area under the curve in the Google trends data.
10. views: movie's mean number of Youtube trailer views.
11. likes: movie's mean number of Youtube trailer likes.
12. dislikes: movie's mean number of Youtube trailer dislikes.
13. dt_main: number of days between the Youtube trailer with largest search volume and the movie's release date.
14. dt_trailers: number of days between the two most popular Youtube trailers for a movie. dt_trailers=0 if the movie only has one trailer, dt_trailers<0 if the first trailer was has the largest search volume.

**Target**
<br>success = opening weekend revenue / budget

**Machine learning**
<br>1, Predict movie success (target) for based on given informations (features) by applying different models
<br>2, Choose the best model (model performance) and interpret the predicted success (feature importance)

**Metrics**
<br>Model performance can be evaluated in different ways, here R2 score is used
<br>R2 score: the proportion of the variance in the dependent variable (target) that is predictable from the independent variables (features). R2 score is no greater than 1 and the higher R2 the better model performance. A negative R2 score suggests that the model performance is worse than mean value prediction, and R2 score of 1 indicates a perfect prediction.
