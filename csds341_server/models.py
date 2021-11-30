# from flask import Flask
from marshmallow import Schema, fields
import datetime
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import func
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

import config


ma = Marshmallow()
db = SQLAlchemy()
Base = automap_base()


class Roles(db.Model):
	__tablename__ = 'Roles'
	role_id = db.Column(db.String(30), primary_key=True)
	edit_perm = db.Column(db.Boolean)
	resp_perm = db.Column(db.Boolean)
	view_resp_perm = db.Column(db.Boolean)


class Subscription(db.Model):
	__tablename__ = 'Subscription'
	subscription_id = db.Column(db.Integer, primary_key=True)
	survey_limit = db.Column(db.Integer)


class User(db.Model):
	__tablename__ = 'Users'
	user_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(40))
	last_name = db.Column(db.String(40))
	email = db.Column(db.String(100), unique=True)
	subscription_id = db.Column(db.Integer, db.ForeignKey('Subscription.subscription_id'))


class Questionnaires(db.Model):
	__tablename__ = 'Questionnaires'
	questionnaire_id = db.Column(db.Integer, primary_key=True)
	number_of_questions = db.Column(db.Integer)


class Questions(db.Model):
	__tablename__ = 'Questions'
	question_id = db.Column(db.Integer, primary_key=True)
	questionnaire_id = db.Column(db.Integer, db.ForeignKey('Questionnaires.questionnaire_id'))
	question_text = db.Column(db.String(400))


class PossibleAnswers(db.Model):
	__tablename__ = 'Possible_Answers'
	option_id = db.Column(db.Integer, primary_key=True)
	question_id = db.Column(db.Integer, db.ForeignKey('Questions.question_id'))
	possible_answer = db.Column(db.String(400))


class Permissions(db.Model):
	__tablename__ = 'Permissions'
	permission_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
	questionnaire_id = db.Column(db.Integer, db.ForeignKey('Questionnaires.questionnaire_id'))
	role_id = db.Column(db.String(30))


class Responses(db.Model):
	__tablename__ = 'Responses'
	response_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
	option_id = db.Column(db.Integer, db.ForeignKey('Possible_Answers.option_id'))
	date_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
