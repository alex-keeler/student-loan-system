from service.base_service import BaseService
from dao.user_dao import UserDao
from dao.student_dao import StudentDao
from domain.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

class UserService(BaseService):
    def __init__(self, user_dao, student_dao, school_billing_official_dao, bank_official_dao, university_dao, bank_dao):
        self.user_dao = user_dao
        self.student_dao = student_dao
        self.school_billing_official_dao = school_billing_official_dao
        self.bank_official_dao = bank_official_dao
        self.university_dao = university_dao
        self.bank_dao = bank_dao

    # gets user by username
    # arguments:
    #   username: username for user (str)
    def get_user_by_username(self, username):
        return self.user_dao.get_user_by_username(username)

    def login(self, username, password):
        """
        Attempts to log in with the given username and password, and returns a boolean representing
        whether the login was successful or not.
        username: The username of the user attempting to login (str)
        password: The password of the user attempting to login (str)
        Returns: A boolean representing if the user was successfully logged in or not (bool)
        """

        # find user in db
        user = self.user_dao.get_user_by_username(username)

        if user != None:
            # password check
            if check_password_hash(user.password_hash, password):
                # store user information in session
                session['logged_in'] = True
                session['user_id'] = user.id
                session['user_type'] = user.user_type
                return True

        return False

    # logs out user
    def logout(self):
        # clear user information from session
        session['logged_in'] = False
        session['user_id'] = None
        session['user_type'] = None

    # registers a new user
    # arguments:
    #   username: username (str)
    #   password: password, before hash (str)
    #   email_address: email address (str)
    #   first_name: first name (str)
    #   last_name: last name (str)
    #   organization_id: student or employee id (str)
    #   date_of_birth: date of birth (date)
    #   user_type: user type (user_type.py)
    # returns: success (boolean)
    def register_user(self, username, password, email_address, first_name, last_name, organization_id, date_of_birth, user_type):

        # make sure a user doesn't exist with that username
        duplicate_username_user = self.user_dao.get_user_by_username(username)
        if (duplicate_username_user != None):
            return False, "A user with that username already exists!"

        # make sure a user doesn't exist with that email
        duplicate_email_user = self.user_dao.get_user_by_email_address(email_address)
        if (duplicate_email_user != None):
            return False, "A user with that email address already exists!"

        # convert password to hash
        password_hash = generate_password_hash(password)

        # register user
        self.user_dao.register_user(username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, user_type)

        return True, ""

    # registers a student based on user
    # arguments:
    #   user_id: id of parent user (int)
    #   credit_score: credit score (int or None)
    #   social_security_last_four: last four digits of social security number (int)
    #   university_id: university id (int)
    # returns: success (boolean)
    def register_student(self, user_id, credit_score, social_security_last_four, university_id):

        # make sure user and university exist
        user = self.user_dao.get_user_by_id(user_id)
        university = self.university_dao.get_university_by_id(university_id)
        if user == None or university == None:
            return False

        # register student
        self.student_dao.register_student(user_id, credit_score, social_security_last_four, university_id)

        return True

    # registers a school billing official based on user
    # arguments:
    #   user_id: id of parent user (int)
    #   university_id: university id (int)
    # returns: success (boolean)
    def register_school_billing_official(self, user_id, university_id):

        # make sure user and university exist
        user = self.user_dao.get_user_by_id(user_id)
        university = self.university_dao.get_university_by_id(university_id)
        if user == None or university == None:
            return False

        # register school billing official
        self.school_billing_official_dao.register_school_billing_official(user_id, university_id)

        return True

    # registers a bank official based on user
    # arguments:
    #   user_id: id of parent user (int)
    #   bank_id: bank id (int)
    # returns: success(boolean)
    def register_bank_official(self, user_id, bank_id):

        # make sure user and bank exist
        user = self.user_dao.get_user_by_id(user_id)
        bank = self.bank_dao.get_bank_by_id(bank_id)
        if user == None or bank == None:
            return False

        # register bank official
        self.bank_official_dao.register_bank_official(user_id, bank_id)

        return True

    # verifies student's last four digits of social security number
    # arguments:
    #   student_user_id: user id of student to check (int)
    #   social_security_last_four: social security to check (int)
    # returns: matching ssn last four (boolean)
    def verify_student_ssn(self, student_user_id, social_security_last_four):
        
        # find student from db, make sure it exists
        student = self.student_dao.get_by_user_id(student_user_id)
        if student == None:
            return False
        
        # compare student ssn last four to provided ssn last four
        if student.social_security_last_four != social_security_last_four:
            return False

        return True

    # gets all students
    # returns: array of students (Student[])
    def get_all_students(self):
        return self.student_dao.get_all_students()