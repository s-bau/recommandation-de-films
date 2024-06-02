import ast
import pandas as pd

# defining a new class "Season" I will use to assign seasons to my list of movies
# only a season-name is necessary - the rest can be defined later
class Season:
    def __init__(self, name):
        self.name = name
        self.timeframe = ""
        self.keywords = {"go": [], "no": []}
        self.genres = {"go": [], "no": []}
        self.release_year = ""
    
    # defining various functions I can call later to assign seasons to movies
    # not every function has to be called - I can choose later what restrictions each season has
    def check_keywords(self, film_synopsis):
        for word in self.keywords["no"]:
            if word in film_synopsis.lower():
                return False
        if self.keywords["go"] == []:
            return True
        for word in self.keywords["go"]:
            if word in film_synopsis.lower():
                return True
        return False
          
    def check_genres(self, film_genres):
        for genre in self.genres["no"]:
            if genre in film_genres:
                return False
        if self.genres["go"] == []:
            return True    
        for genre in self.genres["go"]:
            if genre in film_genres:
                return True
        return False

    def check_release_year(self, rdate):
        if rdate[:4] == self.release_year:
            return True
        return False

# Initializing my seasons and their characteristics
valentine = Season("valentine")
valentine.timeframe = "02/07-02/21"
valentine.genres = {"go": ["Romance"], "no": ["Action", "War", "Documentary"]}

award = Season("award")
award.timeframe = "02/22-03/07"
award.release_year = "2023"

summer = Season("summer")
summer.timeframe = "06/01-08/31"
summer.keywords = {"go": ["summer", "sunshine", "paradise", "vacation"], "no": ["christmas", "winter"]}
summer.genres = {"go": [], "no": ["Documentary"]}

rentree = Season("rentree")
rentree.timeframe = "09/01-09/30"
rentree.keywords = {"go": ["school", "high school"], "no": []}
rentree.genres = {"go": [], "no": ["War"]}

halloween = Season("halloween")
halloween.timeframe = "10/15-11/07"
halloween.keywords = {"go": [], "no": []}
halloween.genres = {"go": ["Horror"], "no": []}

christmas = Season("christmas")
christmas.timeframe = "12/01-01/07"
christmas.keywords = {"go": ["christmas", "winter"], "no": []}


# Function to assign seasons to movies
def set_season(movie):
    seasons = []

    mv_summary = str(movie.iloc[0])
    mv_genres = ast.literal_eval(movie.iloc[1])
    mv_date = str(movie.iloc[2])

    if valentine.check_genres(mv_genres):
        seasons.append(valentine.name)
    
    if award.check_release_year(mv_date):
        seasons.append(award.name)
    
    if rentree.check_keywords(mv_summary) and rentree.check_genres(mv_genres):
        seasons.append(rentree.name)

    if halloween.check_genres(mv_genres):
        seasons.append(halloween.name)
    
    if summer.check_keywords(mv_summary) and summer.check_genres(mv_genres):
        seasons.append(summer.name)

    if christmas.check_keywords(mv_summary):
        seasons.append(christmas.name)
    
    return seasons


# Creating a new df with a seasons column
df_tmdb = pd.read_csv("tmdb_clean.csv", sep = "\t")
df_seasons = df_tmdb.copy()
df_seasons["season"] = df_seasons[["overview", "genres", "release_date", "original_language"]].apply(set_season, axis=1)
df_seasons = df_seasons[(df_seasons["season"].apply(lambda x: len(x) > 0))]
df_seasons = df_seasons[["imdb_id", "original_language", "original_title", "overview", "revenue", "season"]]

# test prints
#test = df_seasons.copy()
#test = test[(test["season"].apply(lambda x: "award" in x))]

# testing with french language films
#test = test[(test["original_language"] == "fr")]

#test = test.sort_values(by=["revenue"], ascending=False)
#for i in range(25):
#    if i == len(test):
#        break
#    print(f"{test.iloc[i,2]}")
#    print(f"{test.iloc[i,3]}")
#    print()

# adding ratings from title_and_ratings
df_rated = pd.read_csv("title_ratings_clean.csv", sep = "\t")
df_all = pd.merge(df_seasons, df_rated, how="left", left_on="imdb_id", right_on="tconst")
df_all.drop(["imdb_id"], axis=1, inplace=True)

# adding french version of titles
df_fr = pd.read_csv("title_akas_clean_fr.csv", sep = "\t")
df_fr = df_fr[["titleId", "title"]]
df_allseasons = pd.merge(df_all, df_fr, how="left", left_on="tconst", right_on="titleId")
df_allseasons.drop(["titleId"], axis=1, inplace=True)
df_allseasons.rename(columns={"title": "titre_fr"}, inplace=True)

# 1 dataframe with all seasons
df_seasons_240428 = pd.DataFrame()
seasons = ["valentine", "award", "summer", "rentree", "halloween", "christmas"]
for season in seasons:
    df = df_allseasons[(df_allseasons["season"].apply(lambda x: season in x))].copy()
    df["season"] = season
    df["original_language"] = df["original_language"].apply(lambda x: "français" if x == "fr" else "étranger")
    df_seasons_240428 = pd.concat([df_seasons_240428, df])
df_seasons_240428.reset_index(drop=True, inplace=True)

# to csv
df_seasons_240428.to_csv("dashboard_seasons.csv", sep = "\t", encoding = "utf-8", index = False)
