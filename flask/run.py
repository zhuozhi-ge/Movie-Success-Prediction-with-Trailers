from flask import Flask, jsonify, request
import json
import numpy as np
import pickle


with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)


@app.route('/')
def index():
    return \
    """
    <!DOCTYPE html>
    <html>
    <body>
    
    <h2>Predict Movie Success with Trailers</h2>
    
    <form method="POST" action="/result">
      Movie Title:<br>
      <input type="text" name="title">
      <br><br>
      
      Movie Release Date:<br>
      Year: <input type="number" name="year"><br>
      Month (Jan. to Dec.: 1 to 12): <input type="number" name="month"><br>
      Weekday (Mon. to Sun.: 0 to 6): <input type="number" name="weekday">
      <br><br>
      
      Running time (at least 80 mins):<br>
      <input type="number" name="runtime" min="80">
      <br><br>
      
      Number of Google Search Peaks (at most 3):<br>
      <input type="number" name="num_peaks" max="3">
      <br><br>
      
      Google Search Volume:<br>
      <input type="number" name="search_volume">
      <br><br>
      
      Days Between Most Searched Youtube Trailer and the Movie Release:<br>
      <input type="number" name="dt_main">
      <br><br>
      
      Days between the Two Most Popular Youtube Trailers:<br>
      <input type="number" name="dt_trailers">
      <br><br>

      Average Youtube Trailer Views:<br>
      <input type="number" name="views">
      <br><br>

      Average Youtube Trailer Likes:<br>
      <input type="number" name="likes">
      <br><br>

      Average Youtube Trailer Dislikes:<br>
      <input type="number" name="dislikes">
      <br><br>

      Production Budget (in dollars):<br>
      <input type="number" name="budget">
      <br><br>
      
      Movie Genres:<br>
      <input type="checkbox" name="g_Drama" value="1">
      <label for="vehicle1"> Drama</label><br>
      <input type="checkbox" name="g_Comedy" value="1">
      <label for="vehicle1"> Comedy</label><br>
      <input type="checkbox" name="g_Thriller" value="1">
      <label for="vehicle1"> Thriller</label><br>
      <input type="checkbox" name="g_Action" value="1">
      <label for="vehicle1"> Action</label><br>
      <input type="checkbox" name="g_Romance" value="1">
      <label for="vehicle1"> Romance</label><br>
      <input type="checkbox" name="g_Adventure" value="1">
      <label for="vehicle1"> Adventure</label><br>
      <input type="checkbox" name="g_Crime" value="1">
      <label for="vehicle1"> Crime</label><br>
      <input type="checkbox" name="g_ScienceFiction" value="1">
      <label for="vehicle1"> ScienceFiction</label><br>
      <input type="checkbox" name="g_Horror" value="1">
      <label for="vehicle1"> Horror</label><br>
      <input type="checkbox" name="g_Family" value="1">
      <label for="vehicle1"> Family</label><br>
      <input type="checkbox" name="g_Mystery" value="1">
      <label for="vehicle1"> Mystery</label><br>
      <input type="checkbox" name="g_Fantasy" value="1">
      <label for="vehicle1"> Fantasy</label><br>
      <input type="checkbox" name="g_Animation" value="1">
      <label for="vehicle1"> Animation</label><br>
      <input type="checkbox" name="g_Music" value="1">
      <label for="vehicle1"> Music</label><br>
      <input type="checkbox" name="g_History" value="1">
      <label for="vehicle1"> History</label><br>
      <input type="checkbox" name="g_War" value="1">
      <label for="vehicle1"> War</label><br>
      <input type="checkbox" name="g_Western" value="1">
      <label for="vehicle1"> Western</label><br>
      <input type="checkbox" name="g_Documentary" value="1">
      <label for="vehicle1"> Documentary</label><br>
      <br>

      <input type="submit" value="Submit">
    </form> 
    </body>
    </html>
    """


@app.route('/result', methods=['POST'])
def result():
    runtime = request.form["runtime"]
    num_peaks = request.form["num_peaks"]
    search_volume = request.form["search_volume"]
    dt_main = request.form["dt_main"]
    dt_trailers = request.form["dt_trailers"]
    
    views = request.form["views"]
    likes = request.form["likes"]
    dislikes = request.form["dislikes"]
    log_views = np.log(int(views))
    log_likes = np.log(int(likes))
    log_dislikes = np.log(int(dislikes))
    
    weekday = request.form["weekday"]
    month = request.form["month"]
    log_budget = np.log(int(request.form["budget"]))
    view_score = np.log(int(views) * (int(likes) - int(dislikes)) / (int(likes) + int(dislikes)) * int(search_volume))
    
    try:
        g_Drama = request.form["g_Drama"]
    except:
        g_Drama = 0
    try:
        g_Comedy = request.form["g_Comedy"]
    except:
        g_Comedy = 0
    try:
        g_Thriller = request.form["g_Thriller"]
    except:
        g_Thriller = 0
    try:
        g_Action = request.form["g_Action"]
    except:
        g_Action = 0
    try:
        g_Romance = request.form["g_Romance"]
    except:
        g_Romance = 0
    try:
        g_Adventure = request.form["g_Adventure"]
    except:
        g_Adventure = 0
    try:
        g_Crime = request.form["g_Crime"]
    except:
        g_Crime = 0
    try:
        g_ScienceFiction = request.form["g_ScienceFiction"]
    except:
        g_ScienceFiction = 0
    try:
        g_Horror = request.form["g_Horror"]
    except:
        g_Horror = 0
    try:
        g_Family = request.form["g_Family"]
    except:
        g_Family = 0
    try:
        g_Mystery = request.form["g_Mystery"]
    except:
        g_Mystery = 0
    try:
        g_Fantasy = request.form["g_Fantasy"]
    except:
        g_Fantasy = 0
    try:
        g_Animation = request.form["g_Animation"]
    except:
        g_Animation = 0
    try:
        g_Music = request.form["g_Music"]
    except:
        g_Music = 0
    try:
        g_History = request.form["g_History"]
    except:
        g_History = 0
    try:
        g_War = request.form["g_War"]
    except:
        g_War = 0
    try:
        g_Western = request.form["g_Western"]
    except:
        g_Western = 0
    try:
        g_Documentary = request.form["g_Documentary"]
    except:
        g_Documentary = 0
    
    X = np.array([[int(runtime), int(num_peaks), int(search_volume), int(dt_main), int(dt_trailers), float(log_views), 
                  float(log_likes), float(log_dislikes), int(weekday), int(month), float(log_budget), int(g_Drama), 
                  int(g_Comedy), int(g_Thriller), int(g_Action), int(g_Romance), int(g_Adventure), int(g_Crime), 
                  int(g_ScienceFiction), int(g_Horror), int(g_Family), int(g_Mystery), int(g_Fantasy), int(g_Animation), 
                  int(g_Music), int(g_History), int(g_War), int(g_Western), int(g_Documentary), float(view_score)]])
    pred = model.predict(X)[0]
    return \
    """
    <!DOCTYPE html>
    <html>
    <body>
    
    The Movie Success (opening weekend revenue / budget) is <br><br>
    {0}<br><br>
    
    <form action="/">
      <input type="submit" value="Recalculate">
    </form> 
    </body>
    </html>
    """.format(pred)


@app.route('/scoring', methods=['POST'])
def get_keywords():
    runtime = request.form["runtime"]
    num_peaks = request.form["num_peaks"]
    search_volume = request.form["search_volume"]
    dt_main = request.form["dt_main"]
    dt_trailers = request.form["dt_trailers"]
    
    views = request.form["views"]
    likes = request.form["likes"]
    dislikes = request.form["dislikes"]
    log_views = np.log(int(views))
    log_likes = np.log(int(likes))
    log_dislikes = np.log(int(dislikes))
    
    weekday = request.form["weekday"]
    month = request.form["month"]
    log_budget = np.log(int(request.form["budget"]))
    view_score = np.log(int(views) * (int(likes) - int(dislikes)) / (int(likes) + int(dislikes)) * int(search_volume))
    
    try:
        g_Drama = request.form["g_Drama"]
    except:
        g_Drama = 0
    try:
        g_Comedy = request.form["g_Comedy"]
    except:
        g_Comedy = 0
    try:
        g_Thriller = request.form["g_Thriller"]
    except:
        g_Thriller = 0
    try:
        g_Action = request.form["g_Action"]
    except:
        g_Action = 0
    try:
        g_Romance = request.form["g_Romance"]
    except:
        g_Romance = 0
    try:
        g_Adventure = request.form["g_Adventure"]
    except:
        g_Adventure = 0
    try:
        g_Crime = request.form["g_Crime"]
    except:
        g_Crime = 0
    try:
        g_ScienceFiction = request.form["g_ScienceFiction"]
    except:
        g_ScienceFiction = 0
    try:
        g_Horror = request.form["g_Horror"]
    except:
        g_Horror = 0
    try:
        g_Family = request.form["g_Family"]
    except:
        g_Family = 0
    try:
        g_Mystery = request.form["g_Mystery"]
    except:
        g_Mystery = 0
    try:
        g_Fantasy = request.form["g_Fantasy"]
    except:
        g_Fantasy = 0
    try:
        g_Animation = request.form["g_Animation"]
    except:
        g_Animation = 0
    try:
        g_Music = request.form["g_Music"]
    except:
        g_Music = 0
    try:
        g_History = request.form["g_History"]
    except:
        g_History = 0
    try:
        g_War = request.form["g_War"]
    except:
        g_War = 0
    try:
        g_Western = request.form["g_Western"]
    except:
        g_Western = 0
    try:
        g_Documentary = request.form["g_Documentary"]
    except:
        g_Documentary = 0
    
    X = np.array([[int(runtime), int(num_peaks), int(search_volume), int(dt_main), int(dt_trailers), float(log_views), 
                  float(log_likes), float(log_dislikes), int(weekday), int(month), float(log_budget), int(g_Drama), 
                  int(g_Comedy), int(g_Thriller), int(g_Action), int(g_Romance), int(g_Adventure), int(g_Crime), 
                  int(g_ScienceFiction), int(g_Horror), int(g_Family), int(g_Mystery), int(g_Fantasy), int(g_Animation), 
                  int(g_Music), int(g_History), int(g_War), int(g_Western), int(g_Documentary), float(view_score)]])
    pred = model.predict(X)[0]
    results = {"success": pred}
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
