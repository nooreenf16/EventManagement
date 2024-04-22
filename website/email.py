from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask, current_app
from flask_mail import Mail, Message
from flask_login import login_user, login_required, logout_user, current_user
from config.configuration import MailConfig 
from .models import Event, Consultation
from datetime import datetime
from website import app

email = Blueprint('email', __name__)
mail = Mail(app)

def sendRegistrationConfirmationEmail(event):
    msg = Message(subject='Event Registratin Confirmation', sender='ctlservices.umsl@gmail.com', recipients=['ctlservices.umsl@gmail.com'])
    msg.html = render_template("email_registration.html", event=event, user=current_user)
    mail.send(msg)

def sendConsultationConfirmationEmail(consultation, type):
    msg = Message(subject='Consultation Creation Confirmation', sender='ctlservices.umsl@gmail.com', recipients=['ctlservices.umsl@gmail.com'])
    if type == "with_staff":    
        msg.html = render_template("email_consultation_staff.html", consultation=consultation, user=current_user)
    else:   
        msg.html = render_template("email_consultation.html", consultation=consultation, user=current_user)
    mail.send(msg)   

def sendPasswordChangedEmail():
    msg = Message(subject='Password Changed Confirmation', sender='ctlservices.umsl@gmail.com', recipients=['ctlservices.umsl@gmail.com'])
    msg.html = render_template("email_password_changed.html", user=current_user)

def sendAdminDecisionToUser(user, requestType, decision):
    print('inside sending decision')
    msg = Message(subject='You request has been processed', sender='ctlservices.umsl@gmail.com', recipients=['ctlservices.umsl@gmail.com'])
    msg.html = render_template("email_admindecision.html", requestType=requestType, decision=decision, user=user)
    mail.send(msg)
    print('sent it!')

#for email sending test purpose
@email.route('/ConsultaionCreationComplete', methods=['GET'])
@login_required
def ConsultaionCreationComplete():
    msg = Message(subject='Hello from the other side!', sender='ctlservices.umsl@gmail.com', recipients=['ctlservices.umsl@gmail.com'])
    userName = "Sam Lin"
    consul = Consultation()
    consul.date = datetime.now()
    consul.category = "test category"
    consul.nature = "test nature"
    consul.hours = 2
    msg.body = "hello {}, your consultation creation is completed.\nConsultanio Date: {}\nConsultation Category: {}\n".format(userName, consul.date, consul.category)
    msg.body = msg.body + "Consultation Nature: {}\nConsultaion hours: {}\n".format(consul.nature, consul.hours)
    mail.send(msg)

# #for email sending test purpose
# @email.route('/ConsultaionCreationComplete', methods=['GET'])
# @login_required
# def ConsultaionCreationComplete():
#     msg = Message(subject='Hello from the other side!', sender='ctlservices.umsl@gmail.com', recipients=['ctlservices.umsl@gmail.com'])
#     userName = "Sam Lin"
#     consul = Consultation()
#     consul.date = datetime.now()
#     consul.category = "test category"
#     consul.nature = "test nature"
#     consul.hours = 2
#     msg.body = "hello {}, your consultation creation is completed.\nConsultanio Date: {}\nConsultation Category: {}\n".format(userName, consul.date, consul.category)
#     msg.body = msg.body + "Consultation Nature: {}\nConsultaion hours: {}\n".format(consul.nature, consul.hours)
#     mail.send(msg)
#     return render_template("email.html", user=current_user)


# @email.route('/EventRegistrationComplete2', methods=['GET'])
# @login_required
# def EventRegistrationComplete2(event):
#     msg = Message(subject='Hello from the other side!', sender='peter@mailtrap.io', recipients=['paul@mailtrap.io'])
#     msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
#     mail.send(msg)
#     return render_template("email.html", user=current_user)

# @email.route('/ConsultaionCreationComplete2', methods=['GET'])
# @login_required
# def ConsultaionCreationComplete2(consultation):
#     msg = Message(subject='Hello from the other side!', sender='peter@mailtrap.io', recipients=['paul@mailtrap.io'])
#     msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
#     mail.send(msg)
#     return render_template("email.html", user=current_user)