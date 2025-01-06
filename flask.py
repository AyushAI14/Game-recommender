from flask import Flask,render_template,request
import pickle

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

with open('model/homedf.pkl', 'rb') as file:
    homedf = pickle.load(file)
with open('model/Maindf.pkl', 'rb') as file:
    Maindf = pickle.load(file)


def genreRecommender(genre):
    if genre in Maindf['genre'].values:
        return Maindf[Maindf['genre'] == genre]
    else:
        return "no genre found"

def titleCheck(title):
    if title.lower() in Maindf['title'].str.lower().values:
        return True
    else:
        return False
# titleCheck('ENLISTeD')

def titlerecommend(title):
  titleChe = titleCheck(title)
  # print(titleChe)
  if titleChe is True:
    genre = Maindf.loc[Maindf['title'].str.lower() == title.lower(), 'genre'].values[0]
    # print(f"The genre for '{title}' is: {genre}")
    if genre in Maindf['genre'].values:
        return Maindf[Maindf['genre'] == genre]

  else:
    print("No title found")
# titlerecommend('ENLISTeD')


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

@app.route("/recommend")
def recommend():
    return render_template("recommend.html")

# @app.route("/UserRecommend", methods=['POST'])
# def genre():
#     user_input_genre = request.form.get('UserinputGenre')
#     filterdata = genreRecommender(user_input_genre)
    
#     if filterdata.empty:  # Check for an empty DataFrame
#         pass
#     else:
#         games = filterdata.to_dict(orient="records")

#     return render_template('recommend.html', games=games, user_input_genre=user_input_genre)
@app.route("/UserRecommend", methods=['POST'])
def title():
    user_input_title = request.form.get('Userinputtitle')
    filterTitleDataframe = titlerecommend(user_input_title)
    if filterTitleDataframe.empty:
        games = []
    else:
        games = filterTitleDataframe.to_dict(orient="records")
    return render_template('recommend.html', games=games, user_input_title=user_input_title)


    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
