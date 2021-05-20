"""Script to seed database."""

import os
import json
from random import choice, randrange
from datetime import datetime

import crud
import model
import server
from pprint import pprint

os.system('dropdb tracker')
os.system('createdb tracker')
model.connect_to_db(server.app, echo=False)
model.db.create_all()

# Load office data from JSON file
with open('data/offices.json') as f:
    office_data = json.loads(f.read())

# pprint(office_data)

office_in_db = []
for office in office_data:
    #unpack each office in office data from json file
    print(office)
    company_name, office_location, office_latitude, office_longitude = (
                                    office['company_name'],
                                    office['office_location'],
                                    office['office_latitude'],
                                    office['office_longitude'])
    

# db_users = crud.create_user

    # create a office and append it to office_in_db
    db_office = crud.create_office(company_name, 
                                    office_location, 
                                    office_latitude,
                                    office_longitude)


    office_in_db.append(db_office)
    model.db.session.add(db_office)
model.db.session.commit()

for n in range(10):
    user = f'user{n+1}@test.com'
    password = 'test'

    # create a user here
    user = crud.create_user(user, password)
    print(user)

    # create 10 ratings for the user
    
    for x in range(1):
        office_code = choice(office_in_db).office_code 
        score = randrange(0,100,20)
        # created_at = datetime.now()
        # print(created_at)
        # print(user.user_id, office_code, score, created_at)
        crud.create_rating( score, office_code, user.user_id)

    