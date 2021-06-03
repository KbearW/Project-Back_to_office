"""Server for back to the office tracker app."""

from flask import (Flask, render_template, request, flash, session, redirect, url_for, jsonify)
from model import connect_to_db, Office
import crud
from sample import geocode
from jinja2 import StrictUndefined
from json import dumps



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
        return redirect('/login')
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
        office_latitude= coordinates[1]
        office_longitude= coordinates[0]
        cpname=crud.get_companyname(company_name)

        if cpname:
            pass
        else:
            # office_location != cpname.office_location
            crud.create_office(company_name, office_location, office_latitude, office_longitude)
            cpname=crud.get_companyname(company_name)
        
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
    officesData = crud.get_all_office_rating()


    return render_template('officeslist.html', officesData = officesData)
    

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
    
    # print('************')
    data = jsonify(crud.get_all_office_rating())
    # coordinates= [(-74.014019, 40.709831),(-122.014019, 37.4810185), (-120, 40), (-90,35)]
    # print('************')
    # print(data)
    # print('************')
    
    return render_template('testing_map.html')


@app.route('/sample2')
def samplemap2():
    data = jsonify(crud.get_all_office_rating())
    return render_template('testing_map2.html', data = data)


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
    coordinates = crud.get_map_data()

    return render_template('testing_map.html', coordinates=coordinates)

@app.route('/sample3')
def testing_map3():
    """View homepage."""
    

    return render_template('testing_map3.html')

@app.route('/sample4')
def testing_map4():
    """View homepage."""
    geojson = crud.get_all_office_rating()


    return render_template('testing_map4.html', geojson=geojson)

@app.route('/sample5')
def testing_map5():
    """View homepage."""
    
    return render_template('testing_map5.html')

@app.route('/sample6')
def testing_map6():
    """View homepage."""
    
    return render_template('testing_map6.html')

@app.route('/sample7')
def testing_map7():
    """View homepage."""

    return render_template('testing_map7-just_cluster.html')


@app.route('/db_data.json')
def db_data():
    """Return db data dictionary."""

    all_offices = crud.get_all_office_rating()
    
    print('~~~~~~~~~~************~~~~~~~~~~')
    print(all_offices)
    
    return jsonify(all_offices)

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
