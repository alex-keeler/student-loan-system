from dao.base_dao import BaseDao
from dao.database import Database
from domain.bank import Bank

class BankDao(BaseDao):
    def __init__(self, db):
        super().__init__(db)

    # fetches bank by id, or None if bank doesn't exist with that id
    # arguments:
    #   bank_id: id (int)
    # returns: bank (Bank)
    def get_bank_by_id(self, bank_id):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, name, address
            FROM bank b
            WHERE b.id = %s
        """)
        parameters = (bank_id,)
        cursor.execute(query, parameters)

        # gather results
        results = []
        for result in cursor:
            results.append(result)

        cursor.close()
        cnx.close()

        # get single result or None, convert to bank object
        bank_data = Database.get_first_or_none(results)
        bank = Bank(*bank_data) if bank_data != None else None

        return bank
    
    # fetches all banks
    # returns: array of banks (Bank[])
    def get_all_banks(self):
        
        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, name, address
            FROM bank b
        """)
        cursor.execute(query)

        # gather results, convert to bank objects
        banks = []
        for result in cursor:
            banks.append(Bank(*result))

        cursor.close()
        cnx.close()

        return banks