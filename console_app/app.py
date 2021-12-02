import mysql.connector
# python -m pip install mysql-connector-python
import os
import time
import datetime

db = mysql.connector.connect(user='csds341', password='admin',
                              host='127.0.0.1',
                              database='csds341_questionnaire')

# basic variables that get used during the functions
cur = db.cursor()
i = ''
sql = ''
val = ''

userID = input("Enter your UserID: ")
print("Thank you! Your user ID will be used to save your responses.")

# function that receives user input, add more print options for more functionalities
def get_user_input():
    print("") # buffer space for readability
    print("[1] To view a list of questionnaires.")
    print("[2] To create a questionnaire.")
    print("[3] To view amount of responses to a questionnaire.")
    print("[4] To respond to a questionnaire.")
    print("[5] Create a new user.")
    print("[q] To quit.")
    print("") # buffer space for readability
    return input("Input: ")

# function that lists questionnaires by ID and their question amount
def view_questionnaire_list():
    sql = "SELECT * FROM questionnaires"
    cur.execute(sql)
    questionnaires = cur.fetchall()
    print("---------------------- Questionnaires ----------------------")
    for q in questionnaires:
        print("ID: " + str(q[0]) + "\tNo. of Questions: " + str(q[1]))
    print("------------------------------------------------------------")

# function that creates a questionnaire, currently has logging info for row IDs whenever something is committed to database
def create_questionnaire():
    questionAmt = input("Enter amount of questions: ")
    
    sql = "INSERT INTO questionnaires (number_of_questions) VALUES (%s)"
    val = (int(questionAmt),)
    cur.execute(sql, val)
    db.commit()
    curQuestionnaireID = cur.lastrowid
    
    # after making the questionnaire, loop to create each question based on the inputted question amount
    for x in range(int(questionAmt)):
        questionText = input("Enter the question text for question " + str(x+1) + ": ")
        
        sql = "INSERT INTO questions (questionnaire_id, question_text) VALUES (%s, %s)"
        val = (curQuestionnaireID, questionText)
        cur.execute(sql, val)
        db.commit()
        curQuestionID = cur.lastrowid
        
        optionAmt = input("Enter the amount of answer choices: ")
        # loop to create options for each question based on the inputted option amount
        for y in range(int(optionAmt)):
            optionText = input("Enter the answer text for option " + str(y+1) + ": ")
            
            sql = "INSERT INTO possible_answers (question_id, possible_answer) VALUES (%s, %s)"
            val = (curQuestionID, optionText)
            cur.execute(sql, val)
            db.commit()

    print("Questionnaire Successfully Created! The Questionnaire ID is " + str(curQuestionnaireID))
    
    # Adds the creator of the questionnaire to permissions table with role creator
    sql = "INSERT INTO permissions (user_id, questionnaire_id, role_id) VALUES (%s, %s, %s)"
    val = (int(userID), int(curQuestionnaireID), "creator")
    cur.execute(sql, val)
    db.commit()
            
# function to view the responses for each question in a questionnaire
def view_responses():
    questionnaireID = input("Enter Questionnaire ID: ")
    
    sql = "SELECT question_id, question_text FROM questions WHERE questionnaire_id = (%s)"
    val = (int(questionnaireID),)
    cur.execute(sql, val)
    questions = cur.fetchall()
    
    # loop for each question in the questionnaire
    for q in questions:
        sql = "SELECT option_id, possible_answer FROM possible_answers WHERE question_id = (%s)"
        val = (int(q[0]),)
        cur.execute(sql, val)
        answers = cur.fetchall()
        
        totalRespondents = 0
        print(q[1])
        # loop for each answer to each question, gives the amount of responses for each answer
        for a in answers:
            sql = "SELECT count(response_id) FROM possible_answers, responses WHERE responses.option_id = possible_answers.option_id AND possible_answers.option_id = (%s) GROUP BY possible_answers.option_id"
            val = (int(a[0]),)
            cur.execute(sql, val)
            count = cur.fetchone()
            if count is None:
                count = 0
            else:
                count = count[0]
            totalRespondents = totalRespondents + int(count)
            print("\t" + a[1] + "\t" + str(count))
            
        print("Total Respondents: " + str(totalRespondents))
        print("")
    
    print("End of Questionnaire's Responses")
        
# function to take a questionnaire, requires questionnaireID
def take_questionnaire():
    questionnaireID = input("Enter Questionnaire ID: ")
    
    sql = "SELECT question_id, question_text FROM questions WHERE questionnaire_id = (%s)"
    val = (int(questionnaireID),)
    cur.execute(sql, val)
    questions = cur.fetchall()
    
    # loop for each question in the questionnaire
    for q in questions:
        sql = "SELECT option_id, possible_answer FROM possible_answers WHERE question_id = (%s)"
        val = (int(q[0]),)
        cur.execute(sql, val)
        answers = cur.fetchall()
        
        print(q[1])
        # loop for each answer to each question, gives the amount of responses for each answer
        for idx, a in enumerate(answers):
            print("\t" + str(idx+1) + ". " + a[1])
        
        # answer chooses and option by inputting the number value on console app
        choice = input("Enter answer choice (digit value): ")
        sql = "INSERT INTO responses (user_id, option_id, date_time) VALUES (%s, %s, %s)"
        val = (int(userID), answers[int(choice)-1][0], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        cur.execute(sql, val)
        db.commit() 
        print("")
        
    print("Questionnaire " + str(questionnaireID) + " Finished. Thank you for sending in your responses!")

# function to add a new user to the database
def add_new_user():
    firstName = input("Enter user's first name: ")
    lastName = input("Enter user's last name: ")
    email = input("Enter user's email address: ")
    sql = "INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)"
    val = (firstName, lastName, email)
    cur.execute(sql, val)
    db.commit()
    newUserID = cur.lastrowid
    print("\nUser successfully created! The assigned User ID is: " + str(newUserID))

# this loop runs until the user inputs 'q' on the take command screen
while i != 'q':
    i = get_user_input()
    
    if i == '1':
        view_questionnaire_list()
    elif i == '2':
        create_questionnaire()
    elif i == '3':
        view_responses()
    elif i == '4':
        take_questionnaire()
    elif i == '5':
        add_new_user()
        

# sample code for querying, visit https://www.w3schools.com/python/python_mysql_getstarted.asp for more info on stuff
# cur.execute("SELECT * FROM Users")
# result = cur.fetchall()

# for x in result:
#     print(x)

db.close()