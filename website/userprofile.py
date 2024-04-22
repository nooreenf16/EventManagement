from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from .models import User, Login, Event
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, logout_user
import json
from website import app, email

userprofile = Blueprint('userprofile', __name__)

@userprofile.route('/user-profile', methods=['GET', 'POST'])
@login_required
def viewUserProfile():
    if request.method == 'GET':
        userInfo = User.query.filter(current_user.id==User.id).first()
        username = Login.query.filter(current_user.id==Login.user_id).first().user_name
        return render_template("user_profile.html", user=current_user, userInfo=userInfo, username=username)

@userprofile.route('/update-user-password', methods=['GET', 'POST'])
@login_required
def updateUserPassword():
    if request.method == 'GET':
        return render_template("update_user_password.html", user=current_user)
    if request.method == 'POST':
        oldPassword = request.form.get('oldPassword')
        newPassword1 = request.form.get('newPassword1')
        newPassword2 = request.form.get('newPassword2')
        oldUserPassword = Login.query.filter(current_user.id==Login.user_id).first().password
        if check_password_hash(oldUserPassword, oldPassword):
            if len(newPassword1) >= 7:
                if newPassword1 == newPassword2:
                    newUserCred = Login.query.filter(current_user.id==Login.user_id).first()
                    newUserCred.password = generate_password_hash(newPassword1, method='sha256')
                    db.session.commit()
                    email.sendPasswordChangedEmail()
                    flash('Password changed, Email sent. Please login again', category='success')
                    logout_user()
                    return redirect(url_for('auth.login'))
                else:
                    flash('New Password don\'t match each other', category='error')
            else:
                flash('Password must be at least 7 chars', category='error')
        else: 
            flash('your input old password does not match current password', category='error')

    return render_template("update_user_password.html", user=current_user)

        

@userprofile.route('/update-user-profile', methods=['GET', 'POST'])
@login_required
def userProfile():
    if request.method == 'GET':
        flash('Leave field blank if no change.', category='success')
        userInfo = User.query.filter(current_user.id==User.id).first()
        username = Login.query.filter(current_user.id==Login.user_id).first().user_name
        return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
    if request.method == 'POST':
        userInfo = User.query.filter(current_user.id==User.id).first()
        currentusercred = Login.query.filter(current_user.id==Login.user_id).first()
        username = Login.query.filter(current_user.id==Login.user_id).first().user_name
        
        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        college = request.form.get('college')
        department = request.form.get('department')
        title = request.form.get('title')
        faculty_appointment = request.form.get('faculty_appointment')
        newusername = request.form.get('username')

        anotherusersxisted = Login.query.filter_by(user_name=newusername).first()
        existedemail = User.query.filter_by(email=email).first()

        if firstname != "":
            if len(firstname) < 2:
                flash('First name must be greater than 1 characters.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            elif not firstname.replace(" ", "").isalpha():
                flash('First name must be all alphabet.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            else:
                userInfo.first_name = firstname
        if lastname != "":
            if len(lastname) < 2:
                flash('Last name must be greater than 1 characters.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            elif not lastname.replace(" ", "").isalpha(): 
                flash('Last name must be all alphabet.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            else:
                userInfo.last_name = lastname
        if email != "":
            if len(email) < 4:
                flash('email must be greater than 4 characters.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            elif not email.find("@"):
                flash('email format is invalid', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            elif existedemail:
                flash('Email already exist.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            else:
                userInfo.email = email
        if phone_number != "":
            if not phone_number.isnumeric():
                flash('Phone number must be all numbers.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            elif len(phone_number) != 10:
                flash('Phone number must be exact 10 numbers.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            else:
                userInfo.phone_number = phone_number
        if department != "":
            if not department.replace(" ", "").isalpha():
                flash('Department must be all alphabet.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            else:
                userInfo.department = department
        if title != "":
            if not title.replace(" ", "").isalpha():
                flash('Title must be all alphabet.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            else:
                userInfo.title = title
        if newusername != "":
            if anotherusersxisted:
                flash('Username already taken, please choose a different one.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            elif len(newusername) < 6:
                flash('Username should be atleast 6 charachters.', category='error')
                return render_template("update_user_profile.html", user=current_user, userInfo=userInfo, username=username)
            else:
                currentusercred.user_name = newusername

        db.session.commit()
        flash('User profile updated', category='success')
        username = Login.query.filter(current_user.id==Login.user_id).first().user_name
        return render_template("user_profile.html", user=current_user, userInfo=userInfo, username=username)
        