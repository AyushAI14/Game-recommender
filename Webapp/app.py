from flask import Flask,render_template,request
import pickle

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

with open('model/homedf.pkl', 'rb') as file:
    homedf = pickle.load(file)
with open('model/Maindf.pkl', 'rb') as file:
    Maindf = pickle.load(file)

@app.route('/')
def home():
    return render_template("home.html",
                           title = list(homedf["title"].values),
                           image = list(homedf["thumbnail"].values),
                           short_description = list(homedf["short_description"].values),
                           game_url = list(homedf["game_url"].values),
                           genre = list(homedf["genre"].values),
                           platform = list(homedf["platform"].values),
                           publisher = list(homedf["publisher"].values),
                           developer = list(homedf["developer"].values),
                           release_date = list(homedf["release_date"].values),
                           freetogame_profile_url = list(homedf["freetogame_profile_url"].values),
                           )

app.route('/genre')
def genre():
    pass

if __name__ == "__main__":
     app.run(debug=True, use_reloader=False)