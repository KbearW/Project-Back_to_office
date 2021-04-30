"""CRUD operations."""

from model import db, User, Office, Rating, connect_to_db


# Functions start here!

def create_user(email_address, passcode):
    """Create and return a new user."""

    new_user = User(email=email_address, password=passcode)

    db.session.add(new_user)
    db.session.commit()

    return new_user
    

def create_office(name, location, latitude, longitude):
    """Create and return a new office."""

    new_office = Office(company_name=name, office_location=location, 
    office_latitude=latitude, office_longitude=longitude)
    
    db.session.add(new_office)
    db.session.commit()

    return new_office

def get_office():
    """Return all office."""

    return Office.query.all()


def get_users():
    """Return all users."""

    return User.query.all()


def create_rating(user_edit, current_office, new_score):
    """Create and return a new rating."""

    new_rating = Rating(user=user_edit, office=current_office, score=new_score)

    db.session.add(new_rating)
    db.session.commit()

    return new_rating

def get_office_by_code(office_code):
    """Get office ID."""
    
    return Office.query.get(office_code)

def get_user_by_id(user_id):
    """Get user by ID."""
    
    return User.query.get(user_id)


def get_user_by_email(email):
    """Get user by email."""
    
    # print('Get version' User.query.get(email))  This doesn't work. Why not? Is it because GET needs to go with Primary Key?
    return User.query.filter(User.email == email).first() # Why use filter rather than the GET query on line#59?



if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)
