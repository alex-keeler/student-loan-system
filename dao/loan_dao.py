from dao.base_dao import BaseDao
from domain.loan import Loan
from dao.database import Database

class LoanDao(BaseDao):
    def __init__(self, db):
        super().__init__(db)

    # creates a new loan entry
    # arguments:
    #   status: loan status (loan_status.py)
    #   bank_loan_offer_id: loan offer id (int)
    #   student_user_id: user id for student (int)
    #   loan_amount: total loan amount (float)
    #   approval_date: approval or rejection date (datetime)
    #   name: nickname for loan (str)
    #   amount_paid: amount paid off loan (int or None)
    #   loan_term_months: loan term in months (int)
    def save_loan(self, status, bank_loan_offer_id, student_user_id, loan_amount, application_date, approval_date, name, amount_paid, loan_term_months):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            INSERT INTO loan
            (status, bank_loan_offer_id, student_user_id, loan_amount, application_date, approval_date, name, amount_paid, loan_term_months)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
        parameters = (status.value, bank_loan_offer_id, student_user_id, loan_amount, application_date, approval_date, name, amount_paid, loan_term_months)
        cursor.execute(query, parameters)

        # commit change
        cnx.commit()

        cursor.close()
        cnx.close()
    
    # fetches all loans for student
    # arguments:
    #   student_user_id: user id for student (int)
    # returns: array of loans (Loan[])
    def get_all_for_student(self, student_user_id):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, status, bank_loan_offer_id, student_user_id, loan_amount, application_date, approval_date, name, amount_paid, loan_term_months
            FROM loan
            WHERE student_user_id = %s
            ORDER BY application_date DESC
        """)
        parameters = (student_user_id,)
        cursor.execute(query, parameters)

        # gather results, convert to loan objects
        loans = []
        for result in cursor:
            loans.append(Loan(*result))

        cursor.close()
        cnx.close()

        return loans

    # fetches all approved loans for student
    # arguments:
    #   student_user_id: user id for student (int)
    # returns: array of loans (Loan[])
    def get_all_approved_for_student(self, student_user_id):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, status, bank_loan_offer_id, student_user_id, loan_amount, application_date, approval_date, name, amount_paid, loan_term_months
            FROM loan
            WHERE student_user_id = %s
            AND status = 'APPROVED'
            ORDER BY application_date DESC
        """)
        parameters = (student_user_id,)
        cursor.execute(query, parameters)

        # gather results, convert to loan objects
        loans = []
        for result in cursor:
            loans.append(Loan(*result))

        cursor.close()
        cnx.close()

        return loans

    # fetches all loans tied to bank official
    # arguments:
    #   bank_official_user_id: user id for bank official (int)
    # returns: array of loans (Loan[])
    def get_all_for_bank_official(self, bank_official_user_id):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT l.id, l.status, l.bank_loan_offer_id, l.student_user_id, l.loan_amount, l.application_date, l.approval_date, l.name, l.amount_paid, l.loan_term_months
            FROM bank_official bo
            JOIN bank b on b.id = bo.bank_id
            JOIN bank_loan_offer blo ON blo.bank_id = b.id
            JOIN loan l ON l.bank_loan_offer_id = blo.id
            WHERE bo.user_id = %s
            ORDER BY l.application_date DESC
        """)
        parameters = (bank_official_user_id,)
        cursor.execute(query, parameters)

        # gather results, convert to loan objects
        loans = []
        for result in cursor:
            loans.append(Loan(*result))

        cursor.close()
        cnx.close()

        return loans

    # fetches all loans with APPLICATION status tied to bank official
    # arguments:
    #   bank_official_user_id: user id for bank official (int)
    # returns: array of loans (Loan[])
    def get_all_applications_for_bank_official(self, bank_official_user_id):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT l.id, l.status, l.bank_loan_offer_id, l.student_user_id, l.loan_amount, l.application_date, l.approval_date, l.name, l.amount_paid, l.loan_term_months
            FROM bank_official bo
            JOIN bank b on b.id = bo.bank_id
            JOIN bank_loan_offer blo ON blo.bank_id = b.id
            JOIN loan l ON l.bank_loan_offer_id = blo.id
            WHERE bo.user_id = %s
            AND l.status = 'APPLICATION'
            ORDER BY l.application_date DESC
        """)
        parameters = (bank_official_user_id,)
        cursor.execute(query, parameters)

        # gather results, convert to loan objects
        loans = []
        for result in cursor:
            loans.append(Loan(*result))

        cursor.close()
        cnx.close()

        return loans

    # fetches loan by id
    # arguments:
    #   loan_id: id (int)
    # returns: loan (Loan)
    def get_loan_by_id(self, loan_id):
        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, status, bank_loan_offer_id, student_user_id, loan_amount, application_date, approval_date, name, amount_paid, loan_term_months
            FROM loan
            WHERE id = %s
        """)
        parameters = (loan_id,)
        cursor.execute(query, parameters)

        # gather results
        results = []
        for result in cursor:
            results.append(result)

        cursor.close()
        cnx.close()

        # get single result or None, convert to loan object
        loan_data = Database.get_first_or_none(results)
        loan = Loan(*loan_data) if loan_data != None else None

        return loan
        
    # updates bank status based on bank officer response
    # arguments:
    #   status: update status (loan_status.py)
    #   loan_id: id of loan to update (int)
    #   approval_date: approval or rejection date (datetime)
    def record_bank_response(self, status, loan_id, approval_date):
        cnx, cursor = self.db.open_connection()
        
        # build and execute query
        query = ("""
            UPDATE loan
            SET status = %s, approval_date = %s
            WHERE id = %s
        """) 
        parameters = (status.value, approval_date, loan_id)
        cursor.execute(query, parameters)
        
        # commit change
        cnx.commit()

        cursor.close()
        cnx.close()