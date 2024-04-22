from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from .models import User, Login, Event
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json
from website import app

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and current_user.is_authenticated:
        flash('You have aleary logged on. Returning to home page.')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        if current_user.is_authenticated:
            flash('You have aleary login')
            return redirect(url_for('view.home'))
        username = request.form.get('username')
        password = request.form.get('password')

        # user = User.query.filter_by(username=username).first()
        usercred = Login.query.filter_by(user_name=username).first()
        if usercred:
            if check_password_hash(usercred.password, password):
                flash('Logged in successfully!', category='success')
                login_user(usercred, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Incorrect username/password.', category='error')
    data = request.form
    print(data)
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET' and current_user.is_authenticated:
        flash('You have already logged in. Returning to home page.')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        if current_user.is_authenticated:
            flash('You have already logged in')
            return redirect(url_for('view.home'))
        email = request.form.get('email')
        confirm_email = request.form.get('confirm_email')
        username = request.form.get('username')
        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        phone_number = request.form.get('phone_number')
        college = request.form.get('college')
        print(college, type(college))
        department = request.form.get('department')
        title = request.form.get('title')
        faculty_appointment = request.form.get('faculty_appointment')
        usertype = "faculty" #default access as general user
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        usercred = Login.query.filter_by(user_name=username).first()
        user = User.query.filter_by(email=email).first()

        if len(firstname) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif len(lastname) < 2:
            flash('Last name must be greater than 1 characters.', category='error')
        elif not firstname.replace(" ", "").isalpha():
            flash('First name must be all alphabet.', category='error')
        elif not lastname.replace(" ", "").isalpha():
            flash('Last name must be all alphabet.', category='error')
        elif len(email) < 4:
            flash('email must be greater than 4 characters.', category='error')
        elif not email.find("@"):
            flash('email format is invalid', category='error')
        elif email != confirm_email:
            flash('Confirm Email doesn\'t match with email', category='error')
        elif phone_number != "" and not phone_number.isnumeric():
            flash('Phone number must be all numbers.', category='error')
        elif phone_number != "" and len(phone_number) != 10:
            flash('Phone number must be exact 10 numbers.', category='error')   
        elif college == None:
            flash('College cannot be empty', category='error')
        elif len(department) == 0:
            flash('Department cannot be empty.', category='error')
        elif not department.replace(" ", "").isalpha():
            flash('Department must be all alphabet.', category='error')
        elif len(title) == 0:
            flash('Title cannot be empty.', category='error')
        elif not title.replace(" ", "").isalpha():
            flash('Title must be all alphabet.', category='error')
        elif user:
            flash('Email already exists.', category='error')
        elif usercred:
            flash('Username already taken, please choose a different one.', category='error')
        elif len(username) < 6:
            flash('Username should be atleast 6 charachters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 chars', category='error')
        else:
            new_user = User(email=email, first_name=firstname, last_name=lastname, phone_number=phone_number, 
                            college=college, department=department, title=title, faculty_appointment=faculty_appointment,
                            user_type=usertype)
            db.session.add(new_user)
            db.session.flush()
            new_usercred = Login(user_name=username,  
                                 password=generate_password_hash(password1, method='sha256'), 
                                 user_id=new_user.id)
            db.session.add(new_usercred)
            db.session.commit()
            
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)