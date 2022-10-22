# student data access object
from dao.base_dao import BaseDao

class SchoolBillingOfficialDao(BaseDao):
    def __init__(self, db):
        super().__init__(db)

    # creates a new school billing official official entry
    # arguments:   
    #   user_id: user id (int)
    #   university_id: university id (int)
    def register_school_billing_official(self, user_id, university_id):
        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            INSERT INTO school_billing_official
            (user_id, university_id)
            VALUES (%s, %s)
             """)
        parameters = (user_id, university_id)
        cursor.execute(query, parameters)

        # commit change
        cnx.commit()

        cursor.close()
        cnx.close()