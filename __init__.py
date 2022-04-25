from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_utils import  ChoiceType
from flask_api import FlaskAPI
from flask_restful import Resource, Api,abort,marshal_with


app = FlaskAPI(__name__)
# app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://VISHWAJIT\SQLEXPRESS/daskha?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret string'
db = SQLAlchemy(app)