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

# new_rating= (score='3', office='abc', user_id='2')

def create_rating(new_score, current_office, user_id):
    """Create and return a new rating."""

    new_rating = Rating(score=new_score, office_code=current_office, user_id=user_id)

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
    
    return User.query.filter(User.email == email).first()



if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)
