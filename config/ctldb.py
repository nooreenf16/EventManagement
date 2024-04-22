from flask import Flask,render_template, request

from config.configuration import Config
from sqlalchemy import create_engine
import mysql.connector


mydb = mysql.connector.connect(user=Config.MYSQL_DATABASE_USER, password=Config.MYSQL_DATABASE_PASSWORD, host=Config.MYSQL_DATABASE_HOST, database=Config.MYSQL_DATABASE_DB)
mysqltemp = "mysql://ctluser:admin@localhost:3306/ctldb"