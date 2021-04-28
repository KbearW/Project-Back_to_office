"""Server for movie ratings app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
#app.secret_key = "SECRET!"

app.jinja_env.undefined = StrictUndefined

app = Flask(__name__)

# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """View all movies."""
    movies = crud.get_movies()
    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)


@app.route('/users')
def all_users():
    """View all users."""
    
    users = crud.get_users()
    return render_template('all_users.html', users=users)


@app.route('/users', methods=['POST'])
def register_user():
    """View all users."""

    email = request.form.get('email')
    password = request.form.get('password')
    
    # Check if this user email is in the database
    user = crud.get_user_by_email(email)
    if user:
        flash('Email is already in use. Try again.')
    else:
        crud.create_user(email, password)
        flash('Account created! Please log in.')

    return redirect('/users')

@app.route('/login', methods=['POST'])
def check_user():

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    movies = crud.get_movies()
    
    if user:
        if password == user.password:
            session['user_id'] = user.user_id
            flash(f"You have been successfully logged in!")
            return render_template('loginpage.html', user=user, movies=movies)
        else:
            flash(f"Wrong password. It should be: {user.password}.")
            return redirect('/')
    else:
        flash("Wrong email. Try again")
        return redirect('/')

@app.route('/login', methods=['GET'])
def process_rating():

    user_id = session['user_id']
    rating = request.args.get('rating')
    user = crud.get_user_by_id(session['user_id'])
    movie= crud.get_movie_by_id(session['movie_id'])

    #Have rating, need to use Session to track user and movie
    crud.create_rating(user, movie, rating)
    return redirect(f'/users/{user_id}')


@app.route('/users/<new_user>')
def new_user(new_user):
    user = crud.get_user_by_id(new_user)

    return render_template('user_profile.html', user=user)

@app.route('/movies/<movie_id>/rate_movie')
def show_rating_page(movie_id):
    """Display movie rating page."""
    movie = crud.get_movie_by_id(movie_id)
    session['movie_id'] = movie_id

    return render_template('rate_movie.html', movie=movie)    


if __name__ == '__main__':
    app.secret_key = "SECRET!" #Why does this work down here but not when it's on line 12? Is this because line 75 runs BEFORE line 12?
    connect_to_db(app,echo=False)
    app.run(host='0.0.0.0', debug=True)
