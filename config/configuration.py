class Config:
    DEBUG = True
    WELCOME_MESSAGE = 'This message is from config class'
    MYSQL_DATABASE_USER = 'ctluser'
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_PASSWORD = 'admin'
    MYSQL_DATABASE_DB = 'ctldb'

class MailConfig:
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT= 587
    MAIL_USERNAME='ctlservices.umsl@gmail.com'
    MAIL_PASSWORD='igbk dgpp anwr cnst'
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
