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

    return new_rating


def get_office():
    """Return all office."""

    return Office.query.all()


def get_users():
    """Return all users."""

    return User.query.all()

def get_ratings_by_office_code(code):
    """Return ratings."""    

# select office_code, created_at from ratings where office_code = '1' order by created_at desc limit 1;
# How to pass back 
    q=db.session.query(Rating.rating)
    return q.filter_by(office_code=code).order_by('office_code').first()


def get_timestamp_by_office_code(code):
    """Return timestampe."""    

# select office_code, created_at from ratings group by 1,2 order by created_at desc; Subquery to follow for the html part
# How to pass back 
    q=db.session.query(Rating.created_at)
    return q.filter_by(office_code=code).order_by(code).first()


def get_coordinates():
    """Return all coordinates."""
    
    return db.session.query(Office.office_latitude, Office.office_longitude).all()


def get_offices():
    """Get offices."""
    
    return Office.query.all()

def get_userid(username):
    """Get users."""
    
    return db.session.query(User.user_id).filter(User.username==username).first()


def get_user_match(username):
    """Get username."""
    
    return db.session.query(User.username).filter(User.username==username).one()


def get_password(username):
    """Get password by username."""
    
    return db.session.query(User.password).filter(User.username==username).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)
