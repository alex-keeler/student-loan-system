from service.base_service import BaseService
from datetime import datetime
from domain.enum.loan_status import LoanStatus

class LoanService(BaseService):
    def __init__(self, loan_dao, bank_loan_offer_dao, bank_dao, student_dao):
        self.loan_dao = loan_dao
        self.bank_loan_offer_dao = bank_loan_offer_dao
        self.bank_dao = bank_dao
        self.student_dao = student_dao

    # gets all current bank loan offers (between start and expiration date)
    # returns: array of current bank loan offers (BankLoanOffer[])
    def get_all_current_bank_loan_offers(self):
        return self.bank_loan_offer_dao.get_all_current()

    # gets current bank loan offer by id (must be between start and expiration date)
    # argument:
    #   bank_loan_offer_id: offer id (int)
    # returns: current bank loan offer (BankLoanOffer)
    def get_current_bank_loan_offer_by_id(self, bank_loan_offer_id):
        return self.bank_loan_offer_dao.get_current_by_id(bank_loan_offer_id)

    # gets all bank loan offers
    # returns: array of bank loan offers (BankLoanOffer[])
    def get_all_bank_loan_offers(self):
        return self.bank_loan_offer_dao.get_all()

    # gets all loans for student
    # arguments:
    #   student_user_id: user id for student (int)
    # returns: array of loans (Loan[])
    def get_all_loans_for_student(self, student_user_id):
        return self.loan_dao.get_all_for_student(student_user_id)

    # gets all approved loans for student
    # arguments:
    #   student_user_id: user id for student (int)
    # returns: array of approved loans (Loan[])
    def get_all_approved_loans_for_student(self, student_user_id):
        return self.loan_dao.get_all_approved_for_student(student_user_id)

    # gets all loans tied to bank official
    # arguments:
    #   bank_official_user_id: user id for bank official (int)
    # returns: array of loans (Loan[])
    def get_all_loans_for_bank_official(self, bank_official_user_id):
        return self.loan_dao.get_all_for_bank_official(bank_official_user_id)

    # gets all loans with status 'APPLICATION' tied to bank official
    # arguments:
    #   bank_official_user_id: user id for bank official (int)
    # returns: array of loan applications (Loan[])
    def get_all_loan_applications_for_bank_official(self, bank_official_user_id):
        return self.loan_dao.get_all_applications_for_bank_official(bank_official_user_id)

    # creates loan entry with status 'APPLICATION'
    # arguments:
    #   student_user_id: user id of student (int)
    #   bank_loan_offer_id: id of chosen loan plan (int)
    #   loan_amount: total loan amount (float)
    #   name: nickname of loan (str)
    #   loan_term_months: loan term in months (int)
    # returns: success (boolean)
    def save_loan_application(self, student_user_id, bank_loan_offer_id, loan_amount, name, loan_term_months):

        # verify student and bank loan offer exist
        student = self.student_dao.get_by_user_id(student_user_id)
        if student is None:
            return False

        # verify that loan offer exists and is current
        bank_loan_offer = self.bank_loan_offer_dao.get_current_by_id(bank_loan_offer_id)
        if bank_loan_offer is None:
            return False

        # save loan application
        self.loan_dao.save_loan(LoanStatus.APPLICATION, bank_loan_offer_id, student_user_id, loan_amount, datetime.today(), None, name, None, loan_term_months)

        return True
        
    # updates loan status to 'APPROVED'
    # arguments:
    #   loan_id: loan to update (int)
    #   approval_date: approval date (datetime)
    # returns: success (boolean)
    def approve_loan(self, loan_id, approval_date):
        # make sure loan exists and has status APPLICATION
        loan = self.loan_dao.get_loan_by_id(loan_id)
        if loan == None:
            return False
        if loan.status != 'APPLICATION':
            return False

        # set bank loan status to APPROVED
        self.loan_dao.record_bank_response(LoanStatus.APPROVED, loan_id, approval_date)
        return True
        
    # updates loan status to 'REJECTED'
    # arguments:
    #   loan_id: loan to update (int)
    #   approval_date: rejection date (datetime)
    # returns: success (boolean)
    def reject_loan(self, loan_id, rejection_date):
        # make sure loan exists and has status APPLICATION
        loan = self.loan_dao.get_loan_by_id(loan_id)
        if loan == None:
            return False
        if loan.status != 'APPLICATION':
            return False

        # set bank loan status to REJECTED
        self.loan_dao.record_bank_response(LoanStatus.REJECTED, loan_id, rejection_date)
        return True
    