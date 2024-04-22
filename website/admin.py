from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, AdminRequest, AdminRequestHistory
from . import db
from flask_login import  current_user
from datetime import *
from website import email
import json

admin = Blueprint('admin', __name__)

    
@admin.route('/admin-request', methods=['POST'])
def requestForAdmin():
    if request.method == 'POST':
       adminRequest = json.loads(request.data)
       requestType = adminRequest['requestType']

       existingAdminRequest = AdminRequest.query.filter(AdminRequest.user_id == current_user.id).all()
 
       if len(existingAdminRequest) == 0: 
            newAdminRequest = AdminRequest(user_id=current_user.id, email=current_user.email, request_type=requestType)
            db.session.add(newAdminRequest)
            db.session.commit()
            flash('Successfully Requested!', category='success') 
       else:
            flash('Aready Requested, wait for decision!', category='error')  
       return "Success"       
    
@admin.route('/admin-decision', methods=['POST'])
def adminDecision():
    #print('inside admin decision')
    if request.method == 'POST':
       if current_user.user_type != 'admin':
          flash('Sorry! You do not have priviledges to access admin page', category='error')
          return redirect(url_for('views.home'))
       adminRequest = json.loads(request.data)
       decision = adminRequest['decision']
       requestId = adminRequest['requestId']

       #print(requestId)

       existingAdminRequest = AdminRequest.query.get(requestId)
 
       #print(existingAdminRequest.email)

       if not existingAdminRequest:
            flash('Admin Request does not exist!', category='error')  
       else: 
            if decision == 'Approved':
                User.query.filter(User.id == existingAdminRequest.user_id).update({User.user_type : existingAdminRequest.request_type})
                
            newAdminRequestHistory = AdminRequestHistory(user_id=existingAdminRequest.id, email=existingAdminRequest.email, 
                                                             request_type=existingAdminRequest.request_type, decision=decision)
            db.session.add(newAdminRequestHistory)
            user = User.query.get(existingAdminRequest.user_id)
            email.sendAdminDecisionToUser(user, existingAdminRequest.request_type, decision) 
            AdminRequest.query.filter(AdminRequest.id==requestId).delete()
            db.session.commit()        
            flash('Decision saved and notified!', category='success')    
       
       return "Success"
    

@admin.route('/admin-request', methods=['GET', 'POST'])
def getallAdminRequest():
     if request.method == 'GET':
          if current_user.user_type != 'admin':
               flash('Sorry! You do not have priviledges to access admin page', category='error')
               return redirect(url_for('views.home'))
          headers = ['User Id', 'Email', 'Request Type']
          adminrequests = AdminRequest.query.all()
          return render_template("admin_requests.html", headers=headers, user=current_user, adminrequests=adminrequests)