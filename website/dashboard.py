from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from .models import User, Login, Event, Consultation, EventRegistration
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json
from datetime import *

dashboard = Blueprint('dashboard', __name__)
app = Flask(__name__)

@dashboard.route('/faculty-dashboard', methods=['GET'])
@login_required 
def faculty_dash():
    if request.method == 'GET':
      events = Event.query.filter(Event.start_date >= datetime.now().strftime("%Y-%m-%d")).limit(4).all()
      reg_events = Event.query.filter(Event.start_date >= datetime.now().strftime("%Y-%m-%d"), EventRegistration.event_id == Event.id, 
                                   EventRegistration.user_id == current_user.id).limit(4).all()
      consultations = Consultation.query.filter(Consultation.user_id == current_user.id, Consultation.date >= datetime.now().strftime("%Y-%m-%d")).all()
      return render_template("faculty_dashboard.html", user=current_user, events=events, reg_events=reg_events, consultations=consultations)
    

@dashboard.route('/ctl-dashboard', methods=['GET'])
@login_required 
def ctl_dash():
    if request.method == 'GET':
      if current_user.user_type != 'ctlstaff' and current_user.user_type != 'admin':
        flash('Sorry! You are not able to access this page')
        return redirect(url_for('views.home'))
      events = Event.query.filter( Event.start_date >= datetime.now().strftime("%Y-%m-%d")).limit(4).all()
      reg_events = Event.query.filter(Event.start_date >= datetime.now().strftime("%Y-%m-%d"), EventRegistration.event_id == Event.id, 
                                   EventRegistration.user_id == current_user.id).limit(4).all()
      consultations = Consultation.query.filter(Consultation.user_id == current_user.id, Consultation.date >= datetime.now().strftime("%Y-%m-%d")).all()
      my_events = Event.query.filter(Event.owner_id == current_user.id).limit(4).all()
      my_consultations = Consultation.query.filter(Consultation.staff_id == current_user.id, Consultation.date >= datetime.now().strftime("%Y-%m-%d")).all()
      return render_template("ctl_dashboard.html", 
                             user=current_user, events=events, reg_events=reg_events, consultations=consultations,
                             my_events=my_events, my_consultations=my_consultations)