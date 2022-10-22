# student data access object
from dao.base_dao import BaseDao

class BankOfficialDao(BaseDao):
    def __init__(self, db):
        super().__init__(db)

    # creates a new bank official entry
    # arguments:   
    #   user_id: user id (int)
    #   bank_id: bank id (int)
    def register_bank_official(self, user_id, bank_id):
        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            INSERT INTO bank_official
            (user_id, bank_id)
            VALUES (%s, %s)
            """)
        parameters = (user_id, bank_id)
        cursor.execute(query, parameters)

        # commit change
        cnx.commit()

        cursor.close()
        cnx.close()