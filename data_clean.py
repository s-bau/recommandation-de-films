import pandas as pd

"""filtering imdb and tmdb database with 3 criteria:
1. startyear >= 1970
2. number of votes >= 10k
3. type == movie"""
# using title.basics as first file to sort through
title_basics_chunks = pd.read_csv("https://datasets.imdbws.com/title.basics.tsv.gz",
                                  sep = "\t",
                                  chunksize = 1000000)
# list to fill with filtered files
title_basics_filtered = []

# reading file in chunks and appending data to list where the type is "movie"
# ...and where the release year is >= 1970
for chunk in title_basics_chunks:
    chunk_withstartyear = chunk.loc[chunk["startYear"] != "\\N"].copy()  # drop all titles that don't have a year listed
    filtered_chunk = chunk_withstartyear.loc[(chunk_withstartyear["titleType"] == "movie")
                                      & (chunk_withstartyear["startYear"].astype(int) >= 1970)]
    title_basics_filtered.append(filtered_chunk)

title_basics_filtered = pd.concat(title_basics_filtered)


"""title_ratings"""
# ratings file
title_ratings_chunks = pd.read_csv("https://datasets.imdbws.com/title.ratings.tsv.gz",
                            sep = "\t",
                            chunksize = 1000000)

# list to fill
title_ratings_clean = []

# go through chunks and selecting rows where:
for chunk in title_ratings_chunks:
    # making sure there are values in nb of votes
    chunk_withvalues = chunk.loc[(chunk["numVotes"] != "\\N")].copy()

    # selecting chunks where movie id is in filtered file
    chunk_intitlebasics = chunk_withvalues.loc[chunk_withvalues["tconst"].isin(title_basics_filtered["tconst"])]

    # filtering by number of votes
    chunk_filtered = chunk_intitlebasics.loc[(chunk_intitlebasics["numVotes"] >= 10000)]
    
    title_ratings_clean.append(chunk_filtered)

title_ratings_clean = pd.concat(title_ratings_clean)

# putting new data into csv file
title_ratings_clean.to_csv("title_ratings_clean.csv", sep = "\t", encoding = "utf-8", index = False)


"""title_basics"""
# accessing clean ratings file to use as reference
# (smaller file - no reading in chunks necessary)
title_basics_clean = title_basics_filtered.loc[title_basics_filtered["tconst"].isin(title_ratings_clean["tconst"])]
title_basics_clean.to_csv("title_basics_clean.csv", sep = "\t", encoding = "utf-8", index = False)


"""title_akas"""
title_akas_chunks = pd.read_csv("https://datasets.imdbws.com/title.akas.tsv.gz",
                            sep = "\t",
                            chunksize = 1000000)

# list to fill
title_akas_clean = []

# go through chunks and selecting rows where:
for chunk in title_akas_chunks:

    chunk_clean = chunk.loc[chunk["titleId"].isin(title_ratings_clean["tconst"])]
    title_akas_clean.append(chunk_clean)

title_akas_clean = pd.concat(title_akas_clean)

# putting new data into csv file
title_akas_clean.to_csv("title_akas_clean.csv", sep = "\t", encoding = "utf-8", index = False)


"""title_crew"""
# cleaning title crew
title_crew_chunks = pd.read_csv("https://datasets.imdbws.com/title.crew.tsv.gz",
                            sep = "\t",
                            chunksize = 1000000)

# list to fill
title_crew_clean = []

# go through chunks and selecting rows where:
for chunk in title_crew_chunks:

    chunk_clean = chunk.loc[chunk["tconst"].isin(title_ratings_clean["tconst"])]
    title_crew_clean.append(chunk_clean)

title_crew_clean = pd.concat(title_crew_clean)

# putting new data into csv file
title_crew_clean.to_csv("title_crew_clean.csv", sep = "\t", encoding = "utf-8", index = False)


"""title_principals"""
title_principals_chunks = pd.read_csv("https://datasets.imdbws.com/title.principals.tsv.gz",
                            sep = "\t",
                            chunksize = 1000000)

# list to fill
title_principals_clean = []

# go through chunks and selecting rows where:
for chunk in title_principals_chunks:

    chunk_clean = chunk.loc[chunk["tconst"].isin(title_ratings_clean["tconst"])]
    title_principals_clean.append(chunk_clean)

title_principals_clean = pd.concat(title_principals_clean)

# putting new data into csv file
title_principals_clean.to_csv("title_principals_clean.csv", sep = "\t", encoding = "utf-8", index = False)


"""name_basics"""
# cleaning name basics
name_basics_chunks = pd.read_csv("https://datasets.imdbws.com/name.basics.tsv.gz",
                            sep = "\t",
                            chunksize = 1000000)

# list to fill
name_basics_clean = []

# reading in chunks
for chunk in name_basics_chunks:

    chunk_clean = chunk.loc[(chunk["nconst"].isin(title_crew_clean["directors"]))\
                            | (chunk["nconst"].isin(title_crew_clean["writers"]))\
                            | (chunk["nconst"].isin(title_principals_clean["nconst"]))]
    name_basics_clean.append(chunk_clean)

name_basics_clean = pd.concat(name_basics_clean)

# putting new data into csv file
name_basics_clean.to_csv("name_basics_clean.csv", sep = "\t", encoding = "utf-8", index = False)


"""tmdb"""
# cleaning tmdb file
tmdb_chunks = pd.read_csv("tmdb_full.csv",
                          sep = ",",
                          chunksize = 1000000)

# list to fill
tmdb_clean = []

# go through chunks and selecting rows where:
for chunk in tmdb_chunks:

    chunk_clean = chunk.loc[chunk["imdb_id"].isin(title_ratings_clean["tconst"])]
    tmdb_clean.append(chunk_clean)

tmdb_clean = pd.concat(tmdb_clean)

# putting new data into csv file
tmdb_clean.to_csv("tmdb_clean.csv", sep = "\t", encoding = "utf-8", index = False)
