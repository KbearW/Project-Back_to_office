"""CRUD operations."""

from model import db, User, Office, Rating, connect_to_db
from datetime import datetime
from flask import jsonify


# Functions start here!

def create_user(username, passcode):
    """Create and return a new user."""

    username = User(username=username, password=passcode)

    db.session.add(username)
    db.session.commit()

    return username
    

def create_office(name, location, latitude, longitude):
    """Create and return a new office."""

    new_office = Office(company_name=name, office_location=location, 
    office_longitude=longitude, office_latitude=latitude)
    
    db.session.add(new_office)
    db.session.commit()

    return new_office


def create_rating(new_score, office_code, user_id):
    """Create and return a new rating."""

    new_rating = Rating(rating=new_score, office_code=office_code, user_id=user_id)

    db.session.add(new_rating)
    db.session.commit()
    print("~~~~New Rating has been created!~~~~")

    return new_rating


def get_office(location):
    """Return all office."""
    all_off=db.session.query(Office.office_location)
    location_only=all_off.filter(Office.office_location == location)

    return location_only.first()


def get_users():
    """Return all users."""

    return User.query.all()


def get_office_code(companyname, officelocation):
    """Return the office code.""" 

    all_office_code=db.session.query(Office.office_code)
    just_co=all_office_code.filter(Office.company_name == companyname, Office.office_location == officelocation)

    return just_co.first()[0]


def get_office_data():
    """Return all coordinates."""
    
    # for each office, retrive the most recent rating per office- use n query
    all_offices = db.session.query(Office.company_name, Office.office_location, Office.office_latitude, Office.office_longitude).all()

    return all_offices

def get_rating_info(office_code):
    """Get rating info."""

    rating_by_company_code = db.session.query( Rating.rating, Rating.created_at).filter_by(office_code=office_code)
    latest_rating = rating_by_company_code.order_by(Rating.created_at.desc()).first()
    # print (latest_rating)
    # print({"rating":latest_rating[0], "timestamp": latest_rating[1]})
    return {"rating":latest_rating[0], "timestamp": latest_rating[1]}


def get_all_office_rating():
    """ Get all office ratings"""
    result = {"type": "FeatureCollection",
                    "features": []
            }

    all_offices = Office.query.all()
    
    for office in all_offices:
        feature = {"type": "Feature", 
            "properties":{
                    "id": office.office_code,
                    "office_location": office.office_location,
                    "office_name": office.company_name, 
                    "rating": get_rating_info(office.office_code)["rating"], 
                    "timestamp": get_rating_info(office.office_code)["timestamp"],
            }, 
            "geometry": {"type": "Point", 
                        "coordinates": [
                        office.office_longitude, office.office_latitude]}}

        result["features"].append(feature)
        print(result)
                    
    return result


def get_map_data():
    """combine get_office_data() and get_rating_info() into one function for jsonify."""
    
    office_data = get_office_data()
    # Q: how to combine the two functions?
    # Sudo Code:
    # 

    # for loop
    # result = 
    
    return office_data


def get_companyname(companyname):
    """Get offices."""
    
    # all_companyname=db.session.query(Office.company_name)
    # targetcompanyname=all_companyname.filter(Office.company_name == companyname)
    return Office.query.filter(Office.company_name == companyname).first()

    # return targetcompanyname.first()


def get_userid(username):
    """Get users."""
    
    return db.session.query(User.user_id).filter(User.username==username).first()


# Something is off for the login function...
def get_user_by_username(username):
    """Get username."""
    # all_users=db.session.query(User.username)
    # user_lookup=all_users.filter(User.username==username)
    return User.query.filter(User.username == username).first()
    # return user_lookup.first()



if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)
