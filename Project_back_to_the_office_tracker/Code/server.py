"""Server for back to the office tracker app."""

from flask import (Flask, render_template, request, flash, session, redirect, url_for)
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


@app.route('/form', methods=['POST', 'GET'])
def form():
    """Input form"""

    if "username" in session:
        username=session['username']
        user_id=crud.get_userid(username)[0]
        print('***********')
        print(f'user_ID: {user_id}')
        if request.method == 'GET':

            return render_template('form.html', username=username, user_id=user_id)
        else:    
            company_name=request.form.get('company_name')
            office_location=request.form.get('office_location')

            rating=int(request.form['rating'])
            # print('************')
            # print(rating)
            # print(type(rating))
            # print('************')
            coordinates=geocode(office_location)
            office_latitude= coordinates[0]
            office_longitude= coordinates[1]

            # check if office exists
            # create a function to get existing office_code or create a new one based on name and locatin
            if:
                # office doesn't exist: (create it)
                crud.create_office(company_name, office_location, office_latitude, office_longitude)
            
            office_code=crud.xxxxx 
            crud.create_rating(rating, office_code, user_id)
            print("username")
            flash(f'You have logged in as {username}!')
            # return render_template('thankyou.html', username=username, user_id=user_id)
            return render_template('thankyou.html')
            else:
                flash(f'Please login/create an account!')
                return render_template('loginpage.html')

@app.route('/officeslist')
def all_offices_list():
    """View all offices in a list."""

    offices = crud.get_offices()
    ratings = crud.get_ratings_by_office_code('1') #how to change this argument to be dynamic coming from officeslist.html?
    # add the sql function here to convert to datetime
    return render_template('officeslist.html', offices=offices, ratings=ratings)
    

@app.route('/officesmap')
def all_offices_map():
    """View all offices in a map."""

    offices = crud.get_offices()

    return render_template('officesmap.html', offices=offices)


@app.route('/sample')
def mapDisplay():
    """Map Display."""
    coordinates= [(-74.014019, 40.709831)]
    # result: [(-73.846739, 40.856809), (-74.014019, 40.709831)]
    # What's the best way to pass the long and lat to the testing_map.html when the return is in a list? and 
    # list=[]
    # for i, coordinate in enumerate (coordinates):
    #     lat=coordinate[i][0]
    #     long=coordinate[i][1]
    #     list.append(lat)


    # office_latitude = crud.get_coordinates()[0]
    # office_longitude = crud.get_coordinates()[1]
    
    # return render_template('testing_map.html', office_latitude= office_latitude, office_longitude= office_longitude)
    return render_template('testing_map.html', coordinates=coordinates)


@app.route('/users')
def all_users():
    """View all users."""
    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Page."""
    if request.method == 'POST':  
        username=request.form.get('username')
        session['username']=username
        password=request.form.get('password')
        session['password']=password
        db_username=crud.get_user_match(username)
        print('*************')
        print(f'db_username: {db_username[0]}')
        db_password=crud.get_password(username)
        print(f'db_password: {db_password[0]}')
        print('*************')

        # if username==db_username and password==db_password:

        
        # else:
        #     crud.create_user(username, password)
        #     session['username'] = username
        #     session['user_id'] = crud.get_user_id(session['username'])
        #     flash(f'You have signup as {username}')
        # flash(f'You have logged in as {username}!')
        return redirect('/')
    else:
        return render_template('loginpage.html')

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

#     username = request.form.get('username')
#     password = request.form.get('password')

#     user = crud.get_user_by_username(username)
#     if user:
#         flash('Cannot create an account with that username. Try again.')
#     else:
#         crud.create_user(username, password)
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
