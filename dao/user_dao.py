# user data access object
from dao.base_dao import BaseDao
from dao.database import Database
from domain.user import User

class UserDao(BaseDao):
    def __init__(self, db):
        super().__init__(db)
        
    # fetches user by username
    # arguments:
    #   username: username for user (str)
    # returns: user (User)
    def get_user_by_username(self, username):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, user_type
            FROM users u
            WHERE u.username = %s
        """)
        parameters = (username,)
        cursor.execute(query, parameters)

        # gather results
        results = []
        for result in cursor:
            results.append(result)

        cursor.close()
        cnx.close()

        # get single result or None, convert to user object
        user_data = Database.get_first_or_none(results)
        user = User(*user_data) if user_data != None else None

        return user

    # fetches user by id
    # arguments:
    #   user_id: id for user (int)
    # returns: user (User)
    def get_user_by_id(self, user_id):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, user_type
            FROM users u
            WHERE u.id = %s
        """)
        parameters = (user_id,)
        cursor.execute(query, parameters)

        # gather results
        results = []
        for result in cursor:
            results.append(result)

        cursor.close()
        cnx.close()

        # get single result or None, convert to user object
        user_data = Database.get_first_or_none(results)
        user = User(*user_data) if user_data != None else None

        return user

    # creates a new user entry
    # arguments:   
    #   username: username (str)
    #   password_hash: hashed password (str)
    #   email_address: email address (str)
    #   first_name: first name (str)
    #   last_name: last name (str)
    #   organization_id: student or employee id (str)
    #   date_of_birth: date of birth (date)
    #   user_type: user type (user_type.py)
    def register_user(self, username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, user_type):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            INSERT INTO users
            (username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, user_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """)
        parameters = (username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, user_type)
        cursor.execute(query, parameters)

        # commit change
        cnx.commit()

        cursor.close()
        cnx.close()
    
    # fetches user by email address
    # arguments:
    #   email_address: email address for user (str)
    # returns: user (User)
    def get_user_by_email_address(self, email_address):

        cnx, cursor = self.db.open_connection()

        query = ("""
            SELECT id, username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, user_type
            FROM users u
            WHERE u.email_address = %s
        """)

        parameters = (email_address,)

        cursor.execute(query, parameters)

        results = []
        for result in cursor:
            results.append(result)

        cursor.close()
        cnx.close()

        user_data = Database.get_first_or_none(results)
        user = User(*user_data) if user_data != None else None

        return user