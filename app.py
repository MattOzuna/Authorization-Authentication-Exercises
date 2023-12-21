from flask import Flask, render_template, flash, redirect, request
from models import db, connect_db
# from forms import AddLoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///authorization"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)
