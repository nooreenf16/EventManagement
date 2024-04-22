from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Login, Event, EventRegistration, AdminRequest, AdminRequestHistory, Consultation
from . import db
from flask_login import  current_user, login_required
from datetime import *
from website import email
import json

event = Blueprint('event', __name__)

@event.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'GET':
        if current_user.user_type != 'ctlstaff' and current_user.user_type != 'admin':
            flash('Sorry! You are not able to access this page')
            return redirect(url_for('views.home'))
        return render_template("event_creation.html", user=current_user)
    
    if request.method == 'POST':
        if current_user.user_type != 'ctlstaff' and current_user.user_type != 'admin':
            flash('Sorry! You are not able to access this page')
            return redirect(url_for('views.home'))
        owner_id = current_user.id
        speaker = request.form.get('speaker')
        start_date = request.form.get('startdate')
        end_date = request.form.get('enddate')
        location = request.form.get('location')
        title = request.form.get('etitle').title()
        type = request.form.get('etype')
        frequency = request.form.get('frequency')
        note = request.form.get('notes')

        event_existing_checker = Event.query.filter_by(title=title).first()
        
        if not title.replace(" ","").isalnum():
            flash('Title name must be either alphabet or numbers', category='error')
        elif(event_existing_checker):
            flash('Event Title alreay existed.', category='error')
        elif title == None:
            flash('Event title cannot be empty', category='error')
        elif not speaker.replace(" ", "").isalpha():
            flash('Speaker\'s name must be all alphabetic', category='error')
        elif not location.replace(" ", "").isalpha():
            flash('Location must be all alphabetic', category='error')
        elif(start_date < datetime.now().strftime("%Y-%m-%d")):
            flash('Event start date cannot be in the past', category='error')
        elif(end_date < datetime.now().strftime("%Y-%m-%d") or end_date < start_date):
            flash('Event end date cannot be in the past or before start date', category='error')
        elif frequency == None:
            flash('Event frequency cannot be empty', category='error')
        else:
            new_event = Event(owner_id=owner_id, start_date=start_date, end_date=end_date, location=location, title=title, type=type, 
                            frequency=frequency, note=note)
            db.session.add(new_event)
            db.session.commit()
            flash('Event created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("event_creation.html", user=current_user)


@event.route('/events', methods=['GET', 'POST'])
def getallevents():
    if request.method == 'GET':
       headers = ['Title', 'Location', 'Start Date', 'End Date', 'Frequency', 'Type']
       events = Event.query.filter(Event.start_date >= datetime.now().strftime("%Y-%m-%d"))
       return render_template("events.html", headers=headers, user=current_user, events=events)
    
@event.route('/registered-events', methods=['GET', 'POST'])
@login_required
def getregisiteredevents():
    if request.method == 'GET':
       headers = ['Title', 'Location', 'Start Date', 'End Date', 'Frequency', 'Type']
       events = Event.query.filter(Event.start_date >= datetime.now().strftime("%Y-%m-%d"), EventRegistration.event_id == Event.id, 
                                   EventRegistration.user_id == current_user.id)
       return render_template("registered_events.html", headers=headers, user=current_user, events=events)

@event.route('/owned-events', methods=['GET', 'POST'])
@login_required
def getcreatedevents():
    if request.method == 'GET':
        if current_user.user_type != 'ctlstaff' and current_user.user_type != 'admin':
            flash('Sorry! You are not able to access this page')
            return redirect(url_for('views.home'))
        headers = ['Title', 'Location', 'Start Date', 'End Date', 'Frequency', 'Type']
        events = Event.query.filter(Event.owner_id == current_user.id)
        return render_template("created_events.html", headers=headers, user=current_user, events=events)
    
@event.route('/event-registration', methods=['POST'])
@login_required
def registerForAnEvent():
    if request.method == 'POST':
       eventinfo = json.loads(request.data)
       eventId = eventinfo['eventId']

       existingEventRegistration = EventRegistration.query.filter(EventRegistration.event_id == eventId, EventRegistration.user_id == current_user.id).all()
 
       if len(existingEventRegistration) == 0: 
            newEventRegistration = EventRegistration(event_id = eventId, user_id=current_user.id, organizer = current_user.first_name)
            db.session.add(newEventRegistration)
            db.session.commit()
            event = Event.query.get(eventId)
            email.sendRegistrationConfirmationEmail(event)
            flash('Successfully Registered! Email has been sent to you.', category='success') 
       else:
            flash('Already Registered for this event!', category='error')  
       return "Success"   

@event.route('/events/<eventId>', methods=['DELETE'])
def delete_event(eventId):
    if request.method == 'DELETE':
        EventRegistration.query.filter(EventRegistration.event_id == eventId).delete(synchronize_session=False)
        Event.query.filter(Event.id == eventId).delete(synchronize_session=False)
        db.session.commit()
        flash('Event Deleted!', category='success')
        return "success"
    
@event.route('/update-event/<eventId>', methods=['GET', 'PUT'])
def update_event(eventId):
    print("inside update event route")
    if request.method == 'GET':
       print(eventId)
       event = Event.query.get(eventId)
       return render_template("update_event.html", event=event, user=current_user)

@event.route('/update-event/<eventId>', methods=['GET','POST'])    
def updateEvent(eventId):
    if request.method == 'POST':
        event = Event.query.get(eventId);  

        if current_user.user_type != 'ctlstaff' and current_user.user_type != 'admin':
            flash('Sorry! You are not able to access this page')
            return redirect(url_for('views.home'))
        speaker = request.form.get('speaker')
        start_date = request.form.get('startdate')
        end_date = request.form.get('enddate')
        location = request.form.get('location')
        title = request.form.get('etitle').title()
        type = request.form.get('etype')
        frequency = request.form.get('frequency')
        note = request.form.get('notes')
        
        if not title.replace(" ","").isalnum():
            flash('Title name must be either alphabet or numbers', category='error')
        elif title == None:
            flash('Event title cannot be empty', category='error')
        elif not speaker.replace(" ", "").isalpha():
            flash('Speaker\'s name must be all alphabetic', category='error')
        elif not location.replace(" ", "").isalpha():
            flash('Location must be all alphabetic', category='error')
        elif(start_date < datetime.now().strftime("%Y-%m-%d")):
            flash('Event start date cannot be in the past', category='error')
        elif(end_date < datetime.now().strftime("%Y-%m-%d") or end_date < start_date):
            flash('Event end date cannot be in the past or before start date', category='error')
        elif frequency == None:
            flash('Event frequency cannot be empty', category='error')
        else:
            event.location = location
            event.title = title
            event.start_date = start_date
            event.end_date = end_date
            event.type = type
            event.frequency = frequency
            event.note = note
        
            db.session.commit()
            flash('Event Updated!', category='success')
            return redirect(url_for('event.getcreatedevents'))
    
        return render_template("update_event.html", event=event, user=current_user)     
  
@event.route('/calendar', methods=['GET', 'POST'])
def calendar():
    all_events = EventRegistration.query.filter_by(user_id=current_user.id).all()
    all_id = [i.event_id for i in all_events]
    print(all_id)
    event_details = Event.query.filter(Event.id.in_(all_id)).all()
    events_json = []
    for e in event_details:
        events_json.append({'title':e.title, 'start':str(e.start_date), 'end':str(e.end_date)})
    print(events_json)
    return render_template("calendar.html", user=current_user, all_events=json.dumps(events_json))
