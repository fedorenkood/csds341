import time

import names
import random
import string

from classes import *


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M:%S', prop)


def output_value(line):
    return "\'" + str(line) + "\'"


if __name__ == '__main__':
    NUM_USERS = 500
    ANSWERS_PER_QUESTIONNAIRE = 1000

    roles = []
    roles.append(Roles('root', True, True, True))
    roles.append(Roles('creator', True, False, True))
    roles.append(Roles('moderator', True, False, False))
    roles.append(Roles('participant', False, True, False))
    roles.append(Roles('analyst', False, False, True))
    roles.append(Roles('guest', False, False, False))

    subscriptions = []
    subscriptions.append(Subscription(1, 5))
    subscriptions.append(Subscription(2, 20))
    subscriptions.append(Subscription(3, 100))

    users = []
    for i in range(NUM_USERS):
        name = names.get_full_name().split(' ')
        subscription = random.choice(subscriptions)
        users.append(User(len(users) + 1, name[0], name[1], subscription.subscription_id))

    questionnaires = []
    questionnaires.append(Questionnaires(len(questionnaires) + 1, 5))
    questionnaires.append(Questionnaires(len(questionnaires) + 1, 7))
    questionnaires.append(Questionnaires(len(questionnaires) + 1, 12))
    questionnaires.append(Questionnaires(len(questionnaires) + 1, 19))
    questionnaires.append(Questionnaires(len(questionnaires) + 1, 25))
    questionnaires.append(Questionnaires(len(questionnaires) + 1, 50))

    example_questions = []
    with open("questions.txt") as file:
        lines = file.readlines()
        for line in lines:
            example_questions.append(line.replace("\'", "\\\'").rstrip())
    questions = []
    for questionnaire in questionnaires:
        for _ in range(questionnaire.number_of_questions):
            question_text = random.choice(example_questions)
            questions.append(Questions(len(questions) + 1, questionnaire.questionnaire_id, question_text))


    possible_answers = []
    for question in questions:
        for _ in range(5):
            chars = "".join([random.choice(string.ascii_letters) for i in range(5)])
            possible_answers.append(PossibleAnswers(len(possible_answers) + 1, question.question_id, chars))

    permissions = []
    for questionnaire in questionnaires:
        creator = random.choice(users)
        left = users.copy()
        left.remove(creator)
        permissions.append(Permissions(len(permissions) + 1, creator.user_id, questionnaire.questionnaire_id, 'creator'))
        role = random.choice([role_1 for role_1 in roles if role_1.role_id != 'creator' and role_1.role_id != 'root'])
        random_1 = random.choice(left)
        left.remove(random_1)
        permissions.append(Permissions(len(permissions) + 1, random_1.user_id, questionnaire.questionnaire_id, role.role_id))
        role = random.choice([role_1 for role_1 in roles if role_1.role_id != 'creator' and role_1.role_id != 'root'])
        random_2 = random.choice(left)
        left.remove(random_2)
        permissions.append(Permissions(len(permissions) + 1, random_2.user_id, questionnaire.questionnaire_id, role.role_id))
        for _ in range(ANSWERS_PER_QUESTIONNAIRE):
            if len(left) > 0:
                random_user = random.choice(left)
                left.remove(random_user)
                permissions.append(Permissions(len(permissions) + 1, creator.user_id, questionnaire.questionnaire_id, 'participant'))

    responses = []
    for permission in permissions:
        if permission.role_id == 'participant':
            related_questions = [q for q in questions if q.questionnaire_id == permission.questionnaire_id]
            date = random_date("2010-01-01 00:00:00", "2021-11-01 00:00:00", random.random())
            for q in related_questions:
                q_answers = [a for a in possible_answers if a.question_id == q.question_id]
                answer = random.choice(q_answers)
                responses.append(Responses(len(responses) + 1, permission.user_id, answer.option_id, str(date)))

    print(users)

    # Print data
    with open('somefile.txt', 'a') as the_file:
        the_file.write("INSERT INTO csds341_questionnaire.Roles(role_id, edit_perm, resp_perm, view_resp_perm)")
        the_file.write("\nVALUES\n")
        for i in range(len(roles)):
            line = "("
            line += output_value(roles[i].role_id) + ","
            line += str(roles[i].edit_perm) + ","
            line += str(roles[i].resp_perm) + ","
            line += str(roles[i].view_resp_perm) + ")"
            if i < len(roles) - 1:
                line += ",\n"
            the_file.write(line)
        the_file.write(";\n\n")

        the_file.write("INSERT INTO csds341_questionnaire.Subscription(subscription_id, survey_limit)")
        the_file.write("\nVALUES\n")
        for i in range(len(subscriptions)):
            line = "("
            line += str(subscriptions[i].subscription_id) + ","
            line += str(subscriptions[i].survey_limit) + ")"
            if i < len(subscriptions) - 1:
                line += ",\n"
            the_file.write(line)
        the_file.write(";\n\n")

        the_file.write("INSERT INTO csds341_questionnaire.Users(user_id, first_name, last_name, email, subscription_id)")
        the_file.write("\nVALUES\n")
        for i in range(len(users)):
            line = "("
            line += str(users[i].user_id) + ","
            line += output_value(users[i].first_name) + ","
            line += output_value(users[i].last_name) + ","
            line += output_value(users[i].email) + ","
            line += output_value(users[i].subscription_id) + ")"
            if i < len(users) - 1:
                line += ",\n"
            the_file.write(line)
        the_file.write(";\n\n")

        the_file.write("INSERT INTO csds341_questionnaire.Questionnaires(questionnaire_id, number_of_questions)")
        the_file.write("\nVALUES\n")
        for i in range(len(questionnaires)):
            line = "("
            line += str(questionnaires[i].questionnaire_id) + ","
            line += str(questionnaires[i].number_of_questions) + ")"
            if i < len(questionnaires) - 1:
                line += ",\n"
            the_file.write(line)
        the_file.write(";\n\n")

        the_file.write("INSERT INTO csds341_questionnaire.Questions(question_id, questionnaire_id, question_text)")
        the_file.write("\nVALUES\n")
        for i in range(len(questions)):
            line = "("
            line += str(questions[i].question_id) + ","
            line += str(questions[i].questionnaire_id) + ","
            line += output_value(questions[i].question_text) + ")"
            if i < len(questions) - 1:
                line += ",\n"
            the_file.write(line)
        the_file.write(";\n\n")

        the_file.write("INSERT INTO csds341_questionnaire.Possible_Answers(option_id, question_id, possible_answer)")
        the_file.write("\nVALUES\n")
        for i in range(len(possible_answers)):
            line = "("
            line += str(possible_answers[i].option_id) + ","
            line += str(possible_answers[i].question_id) + ","
            line += output_value(possible_answers[i].possible_answer) + ")"
            if i < len(possible_answers) - 1:
                line += ",\n"
            the_file.write(line)
        the_file.write(";\n\n")
        
        the_file.write("INSERT INTO csds341_questionnaire.Permissions(permission_id, user_id, questionnaire_id, role_id)")
        the_file.write("\nVALUES\n")
        for i in range(len(permissions)):
            line = "("
            line += str(permissions[i].permission_id) + ","
            line += str(permissions[i].user_id) + ","
            line += str(permissions[i].questionnaire_id) + ","
            line += output_value(permissions[i].role_id) + ")"
            if i < len(permissions) - 1:
                line += ",\n"
            the_file.write(line)
        the_file.write(";\n\n")

        the_file.write("INSERT INTO csds341_questionnaire.Responses(response_id, user_id, option_id, date_time)")
        the_file.write("\nVALUES\n")
        for i in range(len(responses)):
            line = "("
            line += str(responses[i].response_id) + ","
            line += str(responses[i].user_id) + ","
            line += str(responses[i].option_id) + ","
            line += output_value(responses[i].date_time) + ")"
            if i < len(responses) - 1:
                line += ",\n"
            the_file.write(line)
        the_file.write(";\n\n")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
