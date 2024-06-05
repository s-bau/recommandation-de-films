import pandas as pd
import numpy as np
# youtube simplilearn https://www.youtube.com/watch?v=GWFC2_9_iVk

df_recommandation = pd.read_csv('data\data_recommandations.csv', sep='\t', lineterminator='\n')
films = df_recommandation.copy()

# splitting words in synopsis
films["synopsis"] = films["synopsis"].apply(lambda x: x.split())

# putting genres into list
films["genres"] = films["genres"].apply(lambda x: x.replace(",", " "))
films["genres"] = films["genres"].apply(lambda x: x.split())

# same with actors
films["acteurs"] = films["acteurs"].apply(lambda x: x.replace(",", " "))
films["acteurs"] = films["acteurs"].apply(lambda x: x.split())

# creating 1 column with all relevant data as list
films["tags"] = films["synopsis"]+films["genres"]+films["acteurs"]

# creating basic recommnendation df with only the relevant columns
rec_films = films[["id", "titre", "tags"]]

# prepping column for recommendation system
rec_films["tags"] = rec_films["tags"].apply(lambda x: " ".join(x))
rec_films["tags"] = rec_films["tags"].apply(lambda x: x.lower())


"""vectorize data"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(rec_films["tags"]).toarray()
similarity = cosine_similarity(vectors)

# saving np array
np.save("rec.npy", similarity)