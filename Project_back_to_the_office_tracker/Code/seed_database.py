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

    # create a office and append it to office_in_db
    db_office = crud.create_office(company_name, 
                                    office_location, 
                                    office_latitude,
                                    office_longitude)

    # Create a rating for each office
    office_code = crud.get_office_code(company_name, office_location)

    for n in range(2):
        user = f'user{n+1}@{company_name}.com'
        password = 'test'
        user = crud.create_user(user, password)
        score = randrange(0,100,20)
        crud.create_rating( score, office_code, user.user_id)

    office_in_db.append(db_office)
    model.db.session.add(db_office)
model.db.session.commit()

