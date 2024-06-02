import pandas as pd
import numpy as np

rec_films = pd.read_csv('data_recommandations.csv', sep='\t')
similarity = np.load("rec.npy")

def recommend(film):
    film_index = rec_films[rec_films["titre"]==film].index[0]
    distances = similarity[film_index]
    film_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    for i in film_list:
        print(rec_films.iloc[i[0]].titre)
    
    recommendations = []
    for i in film_list:
        recommendations.append(i)
    return recommendations

recommend(input("Titre d'un film : "))