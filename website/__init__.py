from flask import Flask, current_app
from os import path
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config.ctldb import mydb
from config.ctldb import mysqltemp
from config.configuration import MailConfig

db = SQLAlchemy()

app = Flask(__name__)

def create_app():
        
        app.config['SECRET_KEY'] = 'secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = mysqltemp
        app.config['MAIL_SERVER']= MailConfig.MAIL_SERVER
        app.config['MAIL_PORT'] = MailConfig.MAIL_PORT
        app.config['MAIL_USERNAME'] = MailConfig.MAIL_USERNAME
        app.config['MAIL_PASSWORD'] = MailConfig.MAIL_PASSWORD
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USE_SSL'] = False
        
        db.init_app(app)

        from .views import views
        from .auth import auth
        from .email import email
        from .event import event 
        from .dashboard import dashboard
        from .admin import admin
        from .consultation import consultation
 
        from .userprofile import userprofile
        from .reports import reports

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(email, url_prefix='/')
        app.register_blueprint(event, url_prefix='/')
        app.register_blueprint(dashboard, url_prefix='/')
        app.register_blueprint(admin, url_prefix='/')
        app.register_blueprint(consultation, url_prefix='/')
        app.register_blueprint(userprofile, url_prefix='/')
        app.register_blueprint(reports, url_prefix='/')

        from .models import User

        with app.app_context():
                db.create_all()

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
                return User.query.get(int(id)) 

        return app