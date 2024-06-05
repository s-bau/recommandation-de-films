import pandas as pd

df_all = pd.read_csv("title_akas_clean.csv", sep = "\t")
df_en = pd.read_csv("title_basics_clean.csv", sep = "\t")

df_region = df_all[(df_all["region"].apply(lambda x: x == "FR"))]
df_original = df_all[(df_all["region"] != "FR") & (df_all["isOriginalTitle"] == True)]

# merging where region FR and where title is original and title id is not yet in region FR
df_original = df_original[~df_original["titleId"].isin(df_region["titleId"])]
df_fr = pd.concat([df_region, df_original], ignore_index=True)

# looking for duplicates
duplicate_fr = df_fr[df_fr.duplicated(subset="titleId")]
#print(duplicate_fr.sort_values(by="titleId"))

# dropping duplicates (keeping the last)
df_all_fr = df_fr.copy()
df_all_fr.drop_duplicates(subset="titleId", keep="last", inplace=True)

# looking for bad translations with attributes "literal English title"
# comparing them to original titles
df_bad_transl = df_all_fr[df_all_fr["attributes"] == "literal English title"]
#print(df_bad_transl)
df_original = pd.DataFrame()
for i in range(len(df_bad_transl)):
    const = df_bad_transl.iloc[i,0]
    df_original = pd.concat([df_original, df_all[(df_all["titleId"] == const) & (df_all["isOriginalTitle"] == 1)]], ignore_index=True)
#print(df_original)

# choosing original titles over bad translations
# translating 2 popular titles manually (Home Alone and Home Alone 2)
df_original.loc[df_original["titleId"] == "tt0099785", "title"] = "Maman, j'ai raté l'avion!"
df_original.loc[df_original["titleId"] == "tt0104431", "title"] = "Maman, j'ai encore raté l'avion!"
#print(df_original)

# replacing original/manually translated titles with bad translations in data_all_fr
df_all_fr = pd.concat([df_all_fr, df_original], ignore_index=True)
df_all_fr.drop_duplicates(subset="titleId", keep="last", inplace=True)

# test prints
#print(df_all_fr[df_all_fr["attributes"] == "literal English title"])
#print(df_all_fr[df_all_fr["titleId"] == "tt0099785"])
#print(df_en)
#print(df_all_fr)

# turning it into csv file
df_all_fr.to_csv("title_akas_clean_fr.csv", sep = "\t", encoding = "utf-8", index = False)

