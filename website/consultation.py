from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Login, Event, EventRegistration, AdminRequest, AdminRequestHistory, Consultation
from . import db
from flask_login import  current_user, login_required
from datetime import *
from website import email
import json

consultation = Blueprint('consultation', __name__)

@consultation.route('/create-consultation', methods=['GET', 'POST'])
@login_required
def create_consultation():
    if request.method == 'POST':
        user_id = current_user.id
        eventinfo = json.loads(request.data)
        event_id = eventinfo['eventId']
        consultation_existing_checker = Consultation.query.filter(Consultation.user_id == user_id, Consultation.event_id == event_id,
                                                                  Consultation.date>=datetime.now().strftime("%Y-%m-%d"), Consultation.type == "event").first() 
        if not consultation_existing_checker:
            new_consultation = Consultation(user_id=user_id, event_id=event_id, date=datetime.now().strftime("%Y-%m-%d"), type="event" )
            db.session.add(new_consultation)
            db.session.commit()
            email.sendConsultationConfirmationEmail(new_consultation, "") #email
            flash('Consultation created! Email has been sent to you.', category='success')
        else:
           flash("You have already made a consultation request", category="error")
        return "Success"

@consultation.route('/create-consultation-staff', methods=['GET', 'POST'])
@login_required
def create_consultation_with_staff():
    ctl_staff = User.query.filter_by(user_type="ctlstaff")
    if request.method == 'POST':
        user_id = current_user.id
        mode = request.form.get('mode')
        available_days = request.form.getlist('available_days')
        from_time = request.form.get('from_time')
        to_time = request.form.get('to_time')
        staff_id = request.form.get('ctl_id')
        reason = request.form.get('reason')
        consultation_existing_checker = Consultation.query.filter(Consultation.user_id == user_id, Consultation.staff_id == staff_id, 
                                                                  Consultation.date>=datetime.now().strftime("%Y-%m-%d"), Consultation.type == "staff").first() 
        
        if mode == None:
            flash("Please select a mode", category="error")
        elif not len(available_days):
            flash("Please select at least one available day", category="error")
        elif from_time < '08:00':
            flash("Invalid CTL working hour.", category="error")
        elif to_time > '18:00':
            flash("Invalid CTL working hour.", category="error")
        elif to_time < from_time:
            flash("Consultation end time cannot be earlier than start time.", category="error")
        elif not consultation_existing_checker: 
            available_day_joined = ''
            for available_day in available_days:
                available_day_joined = available_day_joined + available_day + ','
            available_day_joined = available_day_joined[:-1]
            
            new_consultation = Consultation(user_id=user_id, date=datetime.now().strftime("%Y-%m-%d"), nature=mode, 
                                                days = available_day_joined, staff_id=staff_id, from_time=from_time, to_time=to_time,
                                                reasons=reason, type="staff")
            db.session.add(new_consultation)
            db.session.commit()
            email.sendConsultationConfirmationEmail(new_consultation, "staff") #email
            flash('Consultation created! Email has been sent to you.', category='success')
            return redirect(url_for('views.home'))
        else:
           flash("You have already made a consultation request", category="error")
    return render_template("create_consultation.html", user=current_user, ctl_staff=ctl_staff)