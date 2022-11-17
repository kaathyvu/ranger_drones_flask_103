from flask import Blueprint, render_template, request, redirect, url_for, flash
from drone_inventory.forms import UserLoginForm
from drone_inventory.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST']) # always going to be a list & always be methods
def signup():
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit(): # from the forms.html method
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data

            user = User(email, first_name, last_name, password=password)
            # Creating a user instantiates an object from our User class in models.py
            # We use the data from the form above to plug into our User class

            db.session.add(user)
            db.session.commit() # Commits user to database -- similar to git add/commit
            
            flash(f"You have successfully created a user account: {email}", "user-created")
            # Creates a flash message for successfully created user

            return redirect(url_for('auth.signin'))
    except:
        raise Exception("Invalid Form Data. Please check your form")

    return render_template('signup.html', form=form)
    # *IMPORTANT* Need form=form because it passes our instantiated form into our render_template
    # If you forget this step, our form will be "undefined"

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email=form.email.data
            password = form.password.data

            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password): #checks if the password from logged_user matches our password in the form
                login_user(logged_user) #uses login_user function from flask
                flash('You successfully logged in via Email/Password', 'auth-success') # auth-success gives category to our flash message
                return redirect(url_for('site.profile'))

            else:
                flash("Your email or password is invalid.", "auth-failed")
                return redirect(url_for('auth.signin'))

    except:
        raise Exception("Invalid Form Data. Please try again")

    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required # This will hide certain pieces of information on the website unless user is logged in
def logout():
    logout_user()
    return redirect(url_for('site.home'))