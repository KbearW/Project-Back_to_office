"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb tracker')
os.system('createdb tracker')
model.connect_to_db(server.app, echo=False)
model.db.create_all()

# Load office data from JSON file
with open('data/offices.json') as f:
    office_data = json.loads(f.read())

office_in_db = []
for office in office_data:
    #unpack each office in office data from json file
    company_name, office_location, coordinates = (office['company_name'],
                                    office['office_location'],
                                    office['coordinates'])

# db_users = crud.create_user

    # create a office and append it to office_in_db
    db_office = crud.create_office(name=company_name, 
                                    location=office_location, 
                                    coordinates=coordinates)


    office_in_db.append(db_office)
    model.db.session.add(db_office)
model.db.session.commit()

for n in range(10):
    email = f'user{n+1}@test.com'  # Voila! A unique email!
    password = 'test'

    # create a user here
    user = crud.create_user(email, password)
    print(user)

    # create 10 ratings for the user
    
    for x in range(1):
        office_code = choice(office_in_db).office_code 
        score = randint(1,5)
        # created_at = current(datetime) -- need to work on this
        print(user.user_id, office_code, score)
        crud.create_rating( score, office_code, user.user_id)

    