"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')
model.connect_to_db(server.app, echo=False)
model.db.create_all()

# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    #unpack each movie in movie data from json file
    title, overview, poster_path = (movie['title'],
                                    movie['overview'],
                                    movie['poster_path'])
    release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')

    # create a movie and append it to movies_in_db
    db_movie = crud.create_movie(title,
                                 overview,
                                 release_date,
                                 poster_path)

    movies_in_db.append(db_movie)


for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    # create a user here
    user = crud.create_user(email, password)

    # create 10 ratings for the user
    for x in range(10):
        movie = choice(movies_in_db) 
        score = randint(1,5)

        crud.create_rating(user, movie, score)