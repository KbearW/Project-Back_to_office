"""Server for back to the office tracker app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, Office
import crud
from sample import geocode
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/about')
def about():
    """Project goal"""

    return render_template('about.html')

@app.route('/form', methods=['GET'])
def form():
    """Input form"""
    user_name='Kerrie'
    user_id=1
    print(session)
    # session['user_name']=user_name
    # session['user_id']=user_id
    # office_longitude=122
    # office_latitude=100
    # # Need office_latitude=latitude, office_longitude=longitude
    # crud.create_office(user_name, office_location, office_longitude, office_latitude)
    return render_template('form.html', user_name=user_name, user_id=user_id)

@app.route('/form', methods=['POST'])
def submit():
#     """Input form"""
    user_name='Kerrie'
    user_id=1
    company_name=request.form.get('company_name')
    office_location=request.form.get('office_location')
    back_to_office_status=request.form.get('back_to_office_status')
    # print(f"L40:{office_location}")
    coordinates=geocode(office_location)
    # print(coordinates)
    # office_longitude=coordinates["office_longitude"]
    # office_latitude=coordinates["office_latitude"]
    # crud.create_office(user_name, office_location)
    crud.create_office(company_name, office_location, coordinates)
    # crud.create_rating(back_to_office_status, office_location, '1')
    
    return render_template('thankyou.html', user_name=user_name, user_id=user_id)

@app.route('/officeslist')
def all_offices_list():
    """View all offices in a list."""

    offices = crud.get_office_by_code()

    return render_template('officeslist.html')

@app.route('/officesmap')
def all_offices_map():
    """View all offices in a map."""

    offices = crud.get_office_by_code()

    return render_template('officesmap.html')

@app.route('/sample')
def mapDisplay():
    """Map Display."""
    Office.query.get(office_latitude,office_longitude)
    office_longitude=request.form.get('office_longitude')
    office_latitude=request.form.get('office_latitude')
    return render_template('testing_map.html', office_longitude=office_longitude, office_latitude=office_latitude)

@app.route('/users')
def all_users():
    """View all users."""
    # session['user_name']=
    # session['user_id']=
    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/login', methods=['GET'])
def login():
    """Login Page."""

    return render_template('loginpage.html')


@app.route('/login', methods=['POST'])
def handle_login():
    """Login."""

    email=request.form['email']
    password=request.form['password']
    session['user_name'] = user_name
    flash(f'You have logged in as {username}!')
    return redirect('/')

@app.route('/testing_map')
def testing_map():
    """View homepage."""

    return render_template('testing_map.html')


# @app.route('/handle-login', methods=['POST'])
# def handle_login():
#     """Log user into application."""

#     username = request.form['username']
#     password = request.form['password']

#     if password == 'let-me-in':   # FIXME
#         session['current_user'] = username
#         flash(f'Logged in as {username}')
#         return redirect('/')

#     else:
#         flash('Wrong password!')
#         return redirect('/login')

# @app.route('/users', methods=['POST'])
# def register_user():
#     """Create a new user."""

#     email = request.form.get('email')
#     password = request.form.get('password')

#     user = crud.get_user_by_email(email)
#     if user:
#         flash('Cannot create an account with that email. Try again.')
#     else:
#         crud.create_user(email, password)
#         flash('Account created! Please log in.')

#     return redirect('/')


# @app.route('/users/<user_id>')
# def show_user(user_id):
#     """Show details on a particular user."""

#     user = crud.get_user_by_id(user_id)

#     return render_template('user_details.html', user=user)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
