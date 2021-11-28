drop table Permissions;
drop table Roles;


/*  This entity describes the roles that are allowed for each permission evel. For
    each role there are different permissions that are dependent on a true or false
    value (BIT) in SQL. For each tuple of user and survey the permission level
    determines what roles they have.  */
CREATE TABLE Roles
(
    role_id varchar(30),
    edit_perm BIT,
    resp_perm BIT,
    view_resp_perm BIT,
    PRIMARY KEY(role_id)
);
/*  This entity describes the permission level of a user for each questionnaire,
    this is part of a ternary relationship between users, questionnaire, and 
    permission. User and Questionnaire entities are not fully participating
    in this table.  */
CREATE TABLE Permissions
(
    permission_id INT,
    user_id INT,
    questionnaire_id INT,
    role_id varchar(30),
    PRIMARY KEY (permission_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id),
    FOREIGN KEY(questionnaire_id) REFERENCES Questionnaires(questionnaire_id),
    FOREIGN KEY(role_id) REFERENCES Roles(role_id)
);
