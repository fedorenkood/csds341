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

@app.route('/', methods=['GET', 'POST'])
def index():
	# users = User.query.filter_by(first_name='Joseph').all()
	return render_template("index.html", data=Questionnaires.query.all())


@app.route('/questionnaire/<id>', methods=['GET', 'POST'])
def questionnaire(id):
    questions = Questions.query.filter_by(questionnaire_id = id).order_by(Questions.question_id).all()
    answers = PossibleAnswers.query.join(Questions, PossibleAnswers.question_id == Questions.question_id).filter_by(questionnaire_id = id).order_by(Questions.question_id).all()
    return render_template("questionnaire.html", questions=questions, answers=answers)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			# TODO: actually output errors
			flash('Invalid username')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		return redirect('all_questionnaires')
	return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
		db.session.add(user)
		db.session.commit()
		if current_user.is_authenticated:
			flash('Add a user')
		else:
			flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template("register.html", form=form)


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5555, debug=True)
