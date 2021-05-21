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
    if "username" in session:
        username=session['username']
        flash(f'You have logged in as {username}!')
    else:
        flash('Welcome, Guest!')
    return render_template('homepage.html')


@app.route('/about')
def about():
    """Project goal"""
    if "username" in session:
        username=session['username']
        flash(f'You have logged in as {username}!')
    else:
        flash('Welcome, Guest!')
    return render_template('about.html')


@app.route('/form', methods=['POST', 'GET'])
def form():
    """Input form"""
    if 'username' not in session:
        flash(f'Reminder: Please login/create an account!')
        return redirect('/loginpage.html')
    else:
        username=session['username']
        user_id=crud.get_userid(username)[0]
        flash(f'You have logged in as {username}!')

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
        cpname=crud.get_companyname(company_name)

        if cpname:
            pass
        else:
            # office_location != cpname.office_location
            crud.create_office(company_name, office_location, office_latitude, office_longitude)
            cpname=crud.get_companyname(company_name)

            print('******************')
            print(crud.create_office(company_name, office_location, office_latitude, office_longitude))
        
        office_code=cpname.office_code

        
        crud.create_rating(rating, office_code, user_id)
        print('*******Completed******')
        return render_template('thankyou.html')
            


@app.route('/officeslist')
def all_offices_list():
    """View all offices in a list."""

    if "username" in session:
        username=session['username']
        flash(f'You have logged in as {username}!')
    else:
        flash('Welcome, Guest!')
    offices = crud.get_offices()
    ratings = crud.get_ratings_by_office_code('1') #how to change this argument to be dynamic coming from officeslist.html?
    # add the sql function here to convert to datetime
    return render_template('officeslist.html', offices=offices, ratings=ratings)
    

@app.route('/officesmap')
def all_offices_map():
    """View all offices in a map."""
    if "username" in session:
        username=session['username']
        flash(f'You have logged in as {username}!')
    else:
        flash('Welcome, Guest!')
    offices = crud.get_offices()

    return render_template('officesmap.html', offices=offices)


@app.route('/sample')
def mapDisplay():
    """Map Display."""
    if "username" in session:
        username=session['username']
        flash(f'You have logged in as {username}!')
    else:
        flash('Welcome, Guest!')
#     lat=coordinate[i][0]
    # coordinates= crud.get_coordinates()
    coordinates= [(-74.014019, 40.709831),(-122.014019, 37.4810185), (-120, 40), (-90,35)]
    print('************')
    print(coordinates)
    print('************')
    
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
    # if "username" in session:
    #     username=session['username']
    #     flash(f'You have logged in as {username}!')
    # else:
    #     flash('Welcome, Guest!')
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        
        user = crud.get_user_by_username(username)

        if user:
            if password == user.password:
                session['username'] = user.username
                session['user_id'] = user.user_id
                
                username=session['username']
                user_id=session['user_id']
                
                flash(f"Hello, {username}! \n You have been successfully logged in!")
                return render_template('homepage.html', username=username, user_id=user_id)
            else:
                flash(f"Wrong password. Try again")
                return render_template('loginpage.html')

        else:
            flash("Username doesn't exist. Try again or create an account")
            return redirect('/')

    else:
        return render_template('loginpage.html')

@app.route('/logout')
def logout():
    session.clear()
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
