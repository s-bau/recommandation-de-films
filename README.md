# Recommandation de films (Film recommendations)

Creation of a Python application containing a movie recommendation system and a dashboard on film characteristics

Group Project 2 at Wild Code School (8 weeks)

* Data preparation and analysis with Pandas (imdb and tmdb datasets)
* Object oriented programming in Python to add an additional "season" column to movie characteristics
* Data visualization in Tableau
* Machine Learning (NLP) for a movie recommendation
* Streamlit as interface for the recommendation system

## Data preparation

The folder **data** contains python code that will create all the necessary csv files that other codefiles use. The code accesses data from **imdb**. In addition, a csv file with data from **tmdb** is necessary to run the code (the file is too large to save on this repository).

## Dashboard (Tableau)

The files starting with **dashboard_** create all the csv files for the dashboard. **images** contains screenshots of the dashboard, which is also accessible on [public.tableau.com](https://public.tableau.com/app/profile/sophie.baumann5050/viz/Filmrecommendations/Gnral).

<img src=images/tableau_1.jpg>
<img src=images/tableau_2.jpg>
<img src=images/tableau_3.jpg>

## Recommendation system

After running the code in the **data** folder, the file **recommandation_nlp_1.py** creates a (large) numpy array for the NLP recommendation system that can be tested with the file **recommandation_nlp_2.py**.
