class Roles:
	def __init__(self, role_id, edit_perm, resp_perm, view_resp_perm):
		self.role_id = role_id
		self.edit_perm = edit_perm
		self.resp_perm = resp_perm
		self.view_resp_perm = view_resp_perm


class Subscription:
	def __init__(self, subscription_id, survey_limit):
		self.subscription_id = subscription_id
		self.survey_limit = survey_limit


class User:
	def __init__(self, user_id, first_name, last_name, subscription_id):
		self.user_id = user_id
		self.first_name = first_name
		self.last_name = last_name
		self.email = (first_name + last_name).lower() + "@gmail.com"
		self.subscription_id = subscription_id


class Questionnaires:
	def __init__(self, questionnaire_id, number_of_questions):
		self.questionnaire_id = questionnaire_id
		self.number_of_questions = number_of_questions


class Questions:
	def __init__(self, question_id, questionnaire_id, question_text):
		self.question_id = question_id
		self.questionnaire_id = questionnaire_id
		self.question_text = question_text


class PossibleAnswers:
	def __init__(self, option_id, question_id, possible_answer):
		self.option_id = option_id
		self.question_id = question_id
		self.possible_answer = possible_answer


class Permissions:
	def __init__(self, permission_id, user_id, questionnaire_id, role_id):
		self.permission_id = permission_id
		self.user_id = user_id
		self.questionnaire_id = questionnaire_id
		self.role_id = role_id


class Responses:
	def __init__(self, response_id, user_id, option_id, date_time):
		self.response_id = response_id
		self.user_id = user_id
		self.option_id = option_id
		self.date_time = date_time
