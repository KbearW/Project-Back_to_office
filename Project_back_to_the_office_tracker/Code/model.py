"""Models for back to the office tracker app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True
                        )
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Office(db.Model):
    """A office datapoint."""

    __tablename__ = 'offices'

    office_code = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True
                        )
    company_name = db.Column(db.String, nullable=False)
    office_location = db.Column(db.Text, nullable=False)
    office_latitude = db.Column(db.Float, nullable=False)
    office_longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Company office_code={self.office_code} location={self.office_location}>'


class Rating(db.Model):
    """Back to office rating."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True
                    )
    score = db.Column(db.Integer)
    office_code = db.Column(db.Integer, db.ForeignKey('offices.office_code'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime)

    office = db.relationship('Office', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'




def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)
