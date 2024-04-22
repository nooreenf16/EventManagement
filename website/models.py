from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Login(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    phone_number = db.Column(db.String(150))
    college = db.Column(db.String(150))
    department = db.Column(db.String(150))
    title = db.Column(db.String(150))
    faculty_appointment = db.Column(db.String(150))
    user_type = db.Column(db.String(150))
    notes = db.relationship('Note')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.DateTime(timezone=True), default=func.now())
    end_date = db.Column(db.DateTime(timezone=True), default=func.now())
    location = db.Column(db.String(150))
    title = db.Column(db.String(150))
    type = db.Column(db.String(150))
    frequency = db.Column(db.String(150))
    note = db.Column(db.String(150))

class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    attend = db.Column(db.Boolean)
    organizer = db.Column(db.String(150))
    
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    nature = db.Column(db.String(150))
    days = db.Column(db.String(150))
    from_time = db.Column(db.String(150))
    to_time = db.Column(db.String(150))
    reasons = db.Column(db.String(150))
    type = db.Column(db.String(150))

class AdminRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String(150), unique=True)
    request_type = db.Column(db.String(150))

class AdminRequestHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    email = db.Column(db.String(150))
    request_type = db.Column(db.String(150))
    decision = db.Column(db.String(150))
    decision_date = db.Column(db.DateTime(timezone=True), default=func.now())

