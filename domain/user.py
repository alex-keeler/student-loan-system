# from databases import Database
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, request, redirect, url_for, flash
from functools import wraps

class User(object):
    def __init__(self, id, username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, user_type):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.organization_id = organization_id
        self.date_of_birth = date_of_birth
        self.user_type = user_type

"""
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| id              | int(11)      | NO   | PRI | NULL    | auto_increment |
| organization_id | varchar(45)  | YES  |     | NULL    |                |
| first_name      | varchar(100) | NO   |     | NULL    |                |
| last_name       | varchar(100) | NO   |     | NULL    |                |
| email_address   | varchar(100) | NO   | UNI | NULL    |                |
| username        | varchar(100) | NO   | UNI | NULL    |                |
| password_hash   | varchar(255) | NO   |     | NULL    |                |
| date_of_birth   | date         | NO   |     | NULL    |                |
| user_type       | varchar(45)  | NO   |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
"""

# page wrapper, requires user to be logged in
def login_required(page):
    """
    A decorator that prevents the user from accessing the page if they are not logged in. They will
    be redirected to the login page, and will be redirected back to the requested page once they
    successfully login.
    Note: The login page function MUST be named login_page()! Otherwise, the decorator will not be
    able to find the correct page to route to.
    """

    @wraps(page)
    def wrapper():
        if not session.get('logged_in'):
            flash("You need to login before viewing this page.")
            return redirect(url_for('login_page', next=request.url))
        return page()
    return wrapper

# page wrapper, requires user to be logged in and of user type 'STUDENT'
def student_only(page):
    @wraps(page)
    def wrapper():
        if not session.get('logged_in'):
            flash("You need to login before viewing this page.")
            return redirect(url_for('login_page', next=request.url))

        if session.get('user_type') != 'STUDENT':
            return redirect(url_for('access_denied_page'))

        return page()
    return wrapper

# page wrapper, requires user to be logged in and of user type 'SCHOOL_BILLING_OFFICIAL'
def school_billing_official_only(page):
    @wraps(page)
    def wrapper():
        if not session.get('logged_in'):
            flash("You need to login before viewing this page.")
            return redirect(url_for('login_page', next=request.url))

        if session.get('user_type') != 'SCHOOL_BILLING_OFFICIAL':
            return redirect(url_for('access_denied_page'))

        return page()
    return wrapper

# page wrapper, requires user to be logged in and of type 'BANK_OFFICIAL'
def bank_official_only(page):
    @wraps(page)
    def wrapper():
        if not session.get('logged_in'):
            flash("You need to login before viewing this page.")
            return redirect(url_for('login_page', next=request.url))

        if session.get('user_type') != 'BANK_OFFICIAL':
            return redirect(url_for('access_denied_page'))

        return page()
    return wrapper