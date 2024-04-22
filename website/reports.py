from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Login, Event, EventRegistration
from . import db
from flask_login import  current_user, login_required
from datetime import *
import json
import pandas as pd
import plotly
import plotly.express as px
from sqlalchemy import func

reports = Blueprint('reports', __name__)

@reports.route('/generate-reports', methods=['GET', 'POST'])
@login_required
def selectTypeOfReports():
    if request.method == 'GET':
        return render_template("select_report_types.html", user=current_user) 
    if request.method == 'POST':
        # Get selected values from the user
        startdate = request.form.get('startdate')
        types = request.form.get('types')

        data = []
        # Query data and create Panda dataframe 
        if types == 'faculty_appoinments':
            result = db.session.query(
                User.faculty_appointment, func.count(User.faculty_appointment)
                ).filter(User.id == EventRegistration.user_id
                        ,Event.id == EventRegistration.event_id
                        ,Event.start_date >= startdate
                ).group_by(User.faculty_appointment).all()
            for i in result:
                data.append(i)
                #print(data)
            df = pd.DataFrame(data,
                        columns=['Faculty Apppoinment', 'Amounts'],
                        index=['a', 'b', 'c'])
            # Create Bar chart
            fig = px.bar(df, x='Faculty Apppoinment', y='Amounts', color='Faculty Apppoinment', barmode='group')
        
        elif types == 'colleges' : 
            result = db.session.query(
                User.college, func.count(User.college)
                ).filter(User.id == EventRegistration.user_id
                        ,Event.id == EventRegistration.event_id
                        ,Event.start_date >= startdate
                ).group_by(User.college).all()
            for i in result:
                data.append(i)
                print(data)
            df = pd.DataFrame(data,
                        columns=['College', 'Amounts'],
                        index=['a', 'b', 'c'])
            # Create Bar chart
            fig = px.bar(df, x='College', y='Amounts', color='College', barmode='group')     
        
        # Create graphJSON
        fig.update_xaxes(ticklabelposition='inside bottom')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
        # Use render_template to pass graphJSON to html
        return render_template('generated_report.html', graphJSON=graphJSON, user=current_user)