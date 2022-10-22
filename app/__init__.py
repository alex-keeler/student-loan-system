from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

from dao.database import Database
from dao.user_dao import UserDao
from dao.student_dao import StudentDao
from dao.school_billing_offical_dao import SchoolBillingOfficialDao
from dao.bank_official_dao import BankOfficialDao
from dao.university_dao import UniversityDao
from dao.bank_dao import BankDao
from dao.bank_loan_offer_dao import BankLoanOfferDao
from dao.loan_dao import LoanDao

from service.user_service import UserService
from service.institution_service import InstitutionService
from service.loan_service import LoanService

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.from_object(Config)

db = Database()

user_dao = UserDao(db)
student_dao = StudentDao(db)
school_billing_official_dao = SchoolBillingOfficialDao(db)
bank_official_dao = BankOfficialDao(db)
university_dao = UniversityDao(db)
bank_dao = BankDao(db)
bank_loan_offer_dao = BankLoanOfferDao(db)
loan_dao = LoanDao(db)

user_service = UserService(user_dao, student_dao, school_billing_official_dao, bank_official_dao, university_dao, bank_dao)
institution_service = InstitutionService(university_dao, bank_dao)
loan_service = LoanService(loan_dao, bank_loan_offer_dao, bank_dao, student_dao)

from app import routes