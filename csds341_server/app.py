from flask import Flask
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import logout_user, login_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from models import *

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.route('/')
def login():  # put application's code here
	# db.session.query()
	users = User.query.filter_by(first_name='Joseph').all()
	return render_template("index.html")


if __name__ == '__main__':
	app.run()
