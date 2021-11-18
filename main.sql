/*  This entity represents users of the questionnaire website. All types of users,
    including people who create questionnaires or answer questionnaires, are in
    this table.  */
CREATE TABLE Users
(
    user_id INT,
    first_name VARCHAR(40),
    last_name VARCHAR(40),
    email VARCHAR(100),
    subscription_id INT,
    PRIMARY KEY(user_id),
    FOREIGN KEY(subscription_id) REFERENCES Subscription(subscription_id)
)


/*  This entity describes the permission level of a user for each questionnaire,
    this is part of a ternary relationship between users, questionnaire, and 
    permission. User and Questionnaire entities are not fully participating
    in this table.  */
CREATE TABLE Permissions
(
    permission_id INT,
    user_id INT,
    questionnaire_id INT,
    role_id INT,
    PRIMARY KEY (permission_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id),
    FOREIGN KEY(questionnaire_id) REFERENCES Questionnaires(questionnaire_id),
    FOREIGN KEY(role_id) REFERENCES Roles(role_id)
)


/*  This entity describes the roles that are allowed for each permission evel. For
    each role there are different permissions that are dependent on a true or false
    value (BIT) in SQL. For each tuple of user and survey the permission level
    determines what roles they have.  */
CREATE TABLE Roles
(
    role_id INT,
    edit_perm BIT,
    resp_perm BIT,
    view_resp_perm BIT,
    PRIMARY KEY(role_id)
)


/*  Describes the subscription level and how many surveys users are allowed to
    create at each subscription level.  */
CREATE TABLE Subscription
(
    subscription_id INT,
    survey_limit INT,
    PRIMARY KEY(subscription_id)
)


/*  Defines a questionnaire with the unique id that will be bound to a user using
    the permissions table.  */
CREATE TABLE Questionnaires
(
    questionnaire_id INT,
    number_of_questions INT,
    PRIMARY KEY(questionnaire_id)
)


/*  Determines questions as they are related to each questionnaire.  */
CREATE TABLE Questions
(
    questioN_id BIGINT,
    questionnaire_id INT,
    question_text VARCHAR(400),
    PRIMARY KEY(question_id),
    FOREIGN KEY(questionnaire_id) REFERENCES Questionnaires(questionnaire_id)
)


/*  Defines possible answers to each question. e.g. for multiple choice questions,
    this will have entries for each possible answer, while for questions like rating
    questions, this place will have the range of rankings available.  */
CREATE TABLE Possible_Answers
(
    option_id BIGINT,
    question_id BIGINT,
    possible_answer VARCHAR(400),
    PRIMARY KEY(option_id),
    FOREIGN KEY(question_id) REFERENCES Questions(question_id)
)


/*  Defines the user response to each of the questions and ties them to the unique
    response option identifier and user id.  */
CREATE TABLE Responses
(
    response_id INT,
    user_id INT,
    option_id BIGINT,
    date_time DATETIME,
    PRIMARY KEY(response_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id),
    FOREIGN KEY(option_id) REFERENCES Possible_Answers(option_id)
)

/* Possible queries:
    • Retrive answer counts per question per questionnaire
    • Distributions of responses to a question based on filters like date
    • Query the number of times the question has been asked vs the response rate
    • Did person hit the limit of the number of questionnaires to create */


/* Check if user answered the survey */
SELECT *
FROM Permissions
WHERE questionnaire_id = "QuestionnaireID"
    AND user_id = "UserID"
    AND role_id = "respondent"

/* Check if user has permission to edit for a specific questionnaire */
SELECT *
FROM Permissions
WHERE questionnaire_id = "QuestionnaireID"
    AND user_id = "UserID"
    AND role_id = "editor"

/* Check if user has permission to see analysis for a specific questionnaire */
SELECT *
FROM Permissions
WHERE questionnaire_id = "QuestionnaireID"
    AND user_id = "UserID"
    AND role_id = "analyzer"


/* Retrieve user answers for a specific questionnaire */
SELECT r.response_id, r.option_id, r.date_time
FROM (Questionnaires as q
    INNER JOIN Questions as q2
        INNER JOIN Possible_Answers as p
            INNER JOIN Responses as r
            on r.option_id = p.option_id
        on p.question_id = q2.question_id
    on q.questionnaire_id = q2.questionnaire_id)
WHERE q.questionnaire_id = "QuestionnaireID"
    AND r.user_id = "UserID"

/* Retrieve questions related to questionnaire */
SELECT *
FROM Questions
WHERE questionnaire_id = "QuestionnaireID"

/* Retrieve possible answers related to question */
SELECT *
FROM Possible_Answers
WHERE question_id = "QuestionID"

/* Number of responses to a specific question */
SELECT count(r.reponse_id)
FROM (Questions as q
    INNER JOIN Possible_Answers as p
        INNER JOIN Responses as r
        on r.option_id = p.option_id
    on p.question_id = q.question_id)
WHERE q.question_id = "QuestionID"