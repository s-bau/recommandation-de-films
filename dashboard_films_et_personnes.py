import pandas as pd

"""top films"""
df_genre = pd.read_csv('data/title_basics_clean.csv', sep = "\t")
df_ratings = pd.read_csv('data/title_ratings_clean.csv', sep = "\t")
df_tmdb = pd.read_csv('data/tmdb_clean.csv', sep = "\t")

# Fusionner df_genre avec df_ratings sur la colonne 'tconst'
merged_df = pd.merge(df_genre, df_ratings, on='tconst')

# Fusionner le résultat avec df_tmdb sur la colonne 'imdb_id'
merged_df = pd.merge(merged_df, df_tmdb, left_on='tconst', right_on='imdb_id')

# Sélectionner les colonnes nécessaires
selected_columns = ['tconst', 'originalTitle', 'startYear', 'original_language', 'averageRating', 'numVotes', 'overview', 'revenue']
merged_df = merged_df[selected_columns]

#print(merged_df)

# to csv
merged_df.to_csv("dashboard_films.csv", sep = "\t", encoding = "utf-8", index = False)


"""top directors"""
df_crew = pd.read_csv('data/title_crew_clean.csv', sep = "\t")
df_principals = pd.read_csv('data/title_principals_clean.csv', sep = "\t")
df_actors = pd.read_csv('data/name_basics_clean.csv', sep = "\t")

# Fusion des réal avec les films et les titres
df_merged_directors_films = pd.merge(df_principals[df_principals['category'] == 'director'], df_genre, on='tconst')
df_merged_directors_films = pd.merge(df_merged_directors_films, df_actors, on='nconst')

# Fusion avec df_ratings pour obtenir les évaluations des films
df_merged_directors_films = pd.merge(df_merged_directors_films, df_ratings, on='tconst')

# Fusion avec df_tmdb pour obtenir les recettes et synopsis des films
df_merged_directors_films = pd.merge(df_merged_directors_films, df_tmdb, how='left', left_on='tconst', right_on='imdb_id')

# Sélectionner les colonnes nécessaires
selected_columns = ['tconst', 'primaryName', 'originalTitle', 'startYear', 'averageRating', 'numVotes', 'overview', 'revenue', 'original_language']
df_merged_directors_films = df_merged_directors_films[selected_columns]

print(df_merged_directors_films)

# to csv
df_merged_directors_films.to_csv("dashboard_directors.csv", sep = "\t", encoding = "utf-8", index = False)


"""acteurs et actrices"""
df_titles = pd.read_csv('data/title_akas_clean.csv', sep = "\t")

df_merged_top_actors = pd.merge(df_principals, df_actors, on='nconst')
df_merged_top_actors = pd.merge(df_merged_top_actors, df_genre, on='tconst')
df_merged_top_actors = pd.merge(df_merged_top_actors, df_ratings, on='tconst')

# Fusion avec df_tmdb pour obtenir les recettes et synopsis des films
df_merged_top_actors = pd.merge(df_merged_top_actors, df_tmdb, how='left', left_on='tconst', right_on='imdb_id')

# Sélectionner les colonnes nécessaires
selected_columns = ['category', 'tconst', 'primaryName', 'originalTitle', 'startYear', 'averageRating', 'numVotes', 'revenue', 'overview', 'original_language']
df_merged_top_actors = df_merged_top_actors[selected_columns]

# Filtrer les lignes pour ne conserver que les acteurs
actors = df_merged_top_actors[df_merged_top_actors['category'].isin(['actor'])]

# Filtrer les lignes pour ne conserver que les actrices
actresses = df_merged_top_actors[df_merged_top_actors['category'].isin(['actress'])]

# to csv
actors.to_csv("dashboard_actors.csv", sep = "\t", encoding = "utf-8", index = False)
actresses.to_csv("dashboard_actresses.csv", sep = "\t", encoding = "utf-8", index = False)