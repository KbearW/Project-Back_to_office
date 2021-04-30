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

# Load office data from JSON file
# with open('data/office.json') as f:
#     office_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
office_in_db = []
# for office in office_data:
#     #unpack each office in office data from json file
#     company_name, office_location, office_latitue, office_longitude = (office['company_name'],
#                                     office['office_location'],
#                                     office['office_latitue'],
#                                     office['office_longitude'])


    # create a office and append it to office_in_db
db_office = crud.create_office(name = 'Facebook', 
                                location = 'MPK 20 1 Facebook Way', 
                                latitude = 37.4810185, 
                                longitude = -122.1550338)

office_in_db.append(db_office)

# for n in range(10):
#     email = f'user{n}@test.com'  # Voila! A unique email!
#     password = 'test'

#     # create a user here
#     user = crud.create_user(email, password)

#     # create 10 ratings for the user
#     for x in range(10):
#         office = choice(office_in_db) 
#         score = randint(1,5)

#         crud.create_rating(user, office, rating)