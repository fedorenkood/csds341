from flask import Flask
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import logout_user, login_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from models import *
from forms import *

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.route('/')
def index():  # put application's code here
	# db.session.query()
	users = User.query.filter_by(first_name='Joseph').all()
	return render_template("index.html")

@app.route('/login')
def login():  # put application's code here
	# db.session.query()
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			flash('Invalid username')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('welcome')
		if user.Is_adm == 1:
			next_page = url_for('AdminWelcome')
		return redirect(next_page)
	return render_template("login.html", form=form)

@app.route('/register')
def register():  # put application's code here
	# db.session.query()
	form = RegistrationForm()
	return render_template("register.html", form=form)


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5555, debug=True)
