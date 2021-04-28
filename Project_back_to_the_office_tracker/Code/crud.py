"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


# Functions start here!

def create_user(e, passcode):
    """Create and return a new user."""

    new_user = User(email=e, password=passcode)

    db.session.add(new_user)
    db.session.commit()

    return new_user
    

def create_movie(name, summary, date, poster):
    """Create and return a new movie."""

    new_movie = Movie(title=name, overview=summary, release_date=date, poster_path=poster)
    
    db.session.add(new_movie)
    db.session.commit()

    return new_movie

def get_movies():
    """Return all movies."""

    return Movie.query.all()


def get_users():
    """Return all users."""

    return User.query.all()


def create_rating(user_edit, current_movie, new_score):
    """Create and return a new rating."""

    new_rating = Rating(user=user_edit, movie=current_movie, score=new_score)

    db.session.add(new_rating)
    db.session.commit()

    return new_rating

def get_movie_by_id(movie_id):
    """Get movies ID."""
    
    return Movie.query.get(movie_id)

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
