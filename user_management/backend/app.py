from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db" 
db = SQLAlchemy(app) 

@app.route("/",methods="GET")
def index():
