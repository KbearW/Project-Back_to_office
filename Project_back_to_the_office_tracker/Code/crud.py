"""CRUD operations."""

from model import db, User, Office, Rating, connect_to_db
from datetime import datetime


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
    office_latitude=latitude, office_longitude=longitude)
    
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


def get_ratings_by_office_code(code):
    """Return ratings.""" - WIP   

    # select office_code, created_at from ratings where office_code = '1' order by created_at desc limit 1;
    # How to pass back 
    q=db.session.query(Rating.rating)
    return q.filter_by(office_code=code).order_by('office_code').first()


def get_office_code(companyname, officelocation):
    """Return the office code.""" 

    all_office_code=db.session.query(Office.office_code)
    just_co=all_office_code.filter(Office.company_name == companyname, Office.office_location == officelocation)

    return just_co.first()[0]


def get_timestamp_by_office_code(code):
    """Return timestampe."""  -WIP  

    # select office_code, created_at from ratings group by 1,2 order by created_at desc; Subquery to follow for the html part
    # How to pass back 
    q=db.session.query(Rating.created_at)
    return q.filter_by(office_code=code).order_by(code).first()


def get_coordinates():
    """Return all coordinates."""
    
    return Office.query.all()


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
