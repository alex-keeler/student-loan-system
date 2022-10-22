from dao.base_dao import BaseDao
from domain.bank_loan_offer import BankLoanOffer
from dao.database import Database

class BankLoanOfferDao(BaseDao):
    def __init__(self, db):
        super().__init__(db)

    # fetches all current loan offers (those between start and expiration date)
    # returns: array of bank loan offers (BankLoanOffer[])
    def get_all_current(self):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, interest_rate, bank_id, interest_type, start_date, expiration_date, title
            FROM bank_loan_offer
            WHERE (start_date IS NULL OR start_date <= NOW())
                AND (expiration_date IS NULL OR expiration_date > NOW())
        """)
        cursor.execute(query)

        # gather results convert to bank loan offer objects
        bank_loan_offers = []
        for result in cursor:
            bank_loan_offers.append(BankLoanOffer(*result))

        cursor.close()
        cnx.close()

        return bank_loan_offers

    # fetches all loan offers
    # returns: list of bank loan offers (BankLoanOffer[])
    def get_all(self):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, interest_rate, bank_id, interest_type, start_date, expiration_date, title
            FROM bank_loan_offer
        """)
        cursor.execute(query)

        # gather results, convert to bank loan offer objects
        bank_loan_offers = []
        for result in cursor:
            bank_loan_offers.append(BankLoanOffer(*result))

        cursor.close()
        cnx.close()

        return bank_loan_offers

    # fetches current loan offer by id (must be between start and expiration date)
    # argument:
    #   bank_loan_offer_id: id (int)
    # returns: bank loan offer (BankLoanOffer)
    def get_current_by_id(self, bank_loan_offer_id):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, interest_rate, bank_id, interest_type, start_date, expiration_date, title
            FROM bank_loan_offer
            WHERE id = %s
                AND (start_date IS NULL OR start_date <= NOW())
                AND (expiration_date IS NULL OR expiration_date > NOW())
        """)
        parameters = (bank_loan_offer_id,)
        cursor.execute(query, parameters)

        # gather results
        results = []
        for result in cursor:
            results.append(result)

        cursor.close()
        cnx.close()

        # get single result or None, convert to bank loan offer object
        bank_loan_offer_data = Database.get_first_or_none(results)
        bank_loan_offer = BankLoanOffer(*bank_loan_offer_data) if bank_loan_offer_data is not None else None

        return bank_loan_offer