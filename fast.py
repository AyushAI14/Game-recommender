from fastapi import FastAPI , Request,Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

with open('model/homedf.pkl', 'rb') as file:
    homedf = pickle.load(file)
with open('model/Maindf.pkl', 'rb') as file:
    Maindf = pickle.load(file)

#Helper functions -------------------------------------------------------------------------------------

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
# -------------------------------------------------------------------------------------

@app.get('/')
def home(request:Request):
    return templates.TemplateResponse("home.html",
                            {'request' : request,
                           'title' : list(homedf["title"].values),
                           'image' : list(homedf["thumbnail"].values),
                           'short_description' : list(homedf["short_description"].values),
                           'game_url' : list(homedf["game_url"].values),
                           'genre' : list(homedf["genre"].values),
                           'platform' : list(homedf["platform"].values),
                           'publisher' : list(homedf["publisher"].values),
                           'developer' : list(homedf["developer"].values),
                           'release_date' : list(homedf["release_date"].values),
                           'freetogame_profile_url' : list(homedf["freetogame_profile_url"].values),
                           })

@app.get("/recommend")
def recommend(request: Request):  # Include the 'request' parameter
    return templates.TemplateResponse("recommend.html", {"request": request})


# @app.post("/UserRecommend")
# def genre(request: Request,UserinputGenre : str = Form(...)):

#     filterdata = genreRecommender(UserinputGenre)
    
    
#     games = filterdata.to_dict(orient="records")

#     return templates.TemplateResponse('recommend.html', {'games': games, 'UserinputGenre':UserinputGenre,'request': request})

@app.post("/UserRecommend")
def title(request: Request,user_input_title : str = Form(...)):
    filterTitleDataframe = titlerecommend(user_input_title)
    if filterTitleDataframe.empty:
        games = []
    else:
        games = filterTitleDataframe.to_dict(orient="records")
    return templates.TemplateResponse('recommend.html', {'games': games, 'user_input_title':user_input_title,'request': request})

