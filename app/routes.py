import imp
import string
from app import app, user_service, institution_service, loan_service
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap
from app.forms import LoanApplicationForm, LoginForm, RegisterUserForm
from domain.user import User, bank_official_only, login_required, school_billing_official_only, student_only
import json
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

"""
--------------
| USER PAGES |
--------------
"""

# login form for user
# arguments:
#   next: url to redirect to after login (optional)
@app.route('/login', methods=['get', 'post'])
def login_page():
    form = LoginForm()
    
    # ran during POST once form data is submitted and validated
    if form.validate_on_submit():
        if user_service.login(form.username.data, form.password.data):
            flash("Succesfully logged in.")
            return redirect(request.args.get('next') or url_for('protected_page'))
        else:
            flash("Invalid username/password combination.")

    return render_template('login_page.html', title="Login", form=form)

# logout
@app.route('/logout')
def logout_page():
    user_service.logout()
    flash("Successfully logged out.")
    return redirect(url_for('login_page'))

# register form
@app.route('/register', methods=['get', 'post'])
def register_user_page():
    form = RegisterUserForm()

    university_list = institution_service.get_all_universities()
    bank_list = institution_service.get_all_banks()

    # create tuples of id and name to populate select field in form
    university_choices = []
    for university in university_list:
        university_choices.append((university.id, university.name))

    bank_choices = []
    for bank in bank_list:
        bank_choices.append((bank.id, bank.name))

    # populate select fields
    form.university.choices = university_choices
    form.bank.choices = bank_choices

    if form.validate_on_submit():
        failed = False
        
        #register user
        register_user_success, register_user_message = user_service.register_user(form.username.data, form.password.data, form.email_address.data, form.first_name.data, form.last_name.data, form.organization_id.data, form.date_of_birth.data, form.user_type.data)
        if not register_user_success:
            flash("User registration failed for " + form.username.data + ": " + register_user_message)
            failed = True

        # register student/school billing official/bank official
        if not failed:
            user = user_service.get_user_by_username(form.username.data)
  
            """
                           no switches?
            ⠀⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝
            ⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
            ⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
            ⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
            ⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
            ⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀⠀⠀⠀⠀⠀⠀⠀
            """     
            if user.user_type == 'STUDENT':
                if not user_service.register_student(user.id, None, form.social_security_last_four.data, form.university.data):
                    flash("Student registration failed for " + form.username.data)
                    failed = True
            elif user.user_type == 'SCHOOL_BILLING_OFFICIAL':
                if not user_service.register_school_billing_official(user.id, form.university.data):
                    flash("School billing official registration failed for " + form.username.data)
                    failed = True
            elif user.user_type == 'BANK_OFFICIAL':
                if not user_service.register_bank_official(user.id, form.bank.data):
                    flash("Bank official registration failed for " + form.username.data)
                    failed = True
            else:
                flash("User type not recognized for " + user.user_type)
                failed = True
        
        # show success or error message
        if not failed:
            flash("User added successfully.")
            return redirect(url_for('login_page'))
        else:
            flash("An error occurred while adding the user.")
    else:
        # display errors
        if len(form.errors) > 0:
            print('got error: ', form.errors)

    return render_template('register_user_page.html', title="Add User", form=form)

# demo page, accessible by logged in users
@app.route('/protected-page')
@login_required
def protected_page():
    return render_template('protected_page.html', title="Protected Page")

"""
-----------------
| STUDENT PAGES |
-----------------
"""

# demo page, accessible by students
@app.route('/student-page')
@student_only
def student_page():
    return render_template("student_page.html", title="Student Page")

# allows student to choose loan plan to apply for
@app.route('/select-bank-loan-offer')
@student_only
def select_bank_loan_offer_page():

    loan_offers = loan_service.get_all_current_bank_loan_offers()
    banks = institution_service.get_all_banks()

    # allows for reference to bank object based on loan_offer.bank_id
    bank_dict = {}
    for bank in banks:
        bank_dict[bank.id] = bank

    return render_template("select_bank_loan_offer.html", title="Select Bank Loan Offer", loan_offers=loan_offers, bank_dict=bank_dict)

# student loan overview page
@app.route('/review-bank-loan')
@student_only
def review_bank_loan_page():
    loans = loan_service.get_all_loans_for_student(session['user_id'])
    banks = institution_service.get_all_banks()
    loan_offers = loan_service.get_all_current_bank_loan_offers()

    # allows for reference to bank object based on loan_offer.bank_id
    bank_dict = {}
    for bank in banks:
        bank_dict[bank.id] = bank

    # allows for reference to bank_loan_offer object based on loan.bank_loan_offer_id
    loan_offers_dict = {}
    for loan_offer in loan_offers:
        loan_offers_dict[loan_offer.id] = loan_offer
    
    return render_template("review_bank_loan.html", title = "Review Bank Loans", loans = loans, bank_dict = bank_dict, loan_offers_dict = loan_offers_dict)

# loan application form
# arguments:
#   bank_loan_offer_id: selected bank loan offer id (required)
@app.route('/loan-application', methods=['GET', 'POST'])
@student_only
def loan_application_page():

    bank_loan_offer_id = request.args.get('bank_loan_offer_id')
    bank_loan_offer = loan_service.get_current_bank_loan_offer_by_id(bank_loan_offer_id)

    # if offer doesn't exist or is expired, show access denied page
    if bank_loan_offer == None:
        return render_template("access_denied.html", title="Access Denied")

    bank = institution_service.get_bank_by_id(bank_loan_offer.bank_id)

    form = LoanApplicationForm()
    form.bank_loan_offer_id.data = bank_loan_offer.id
    form.student_user_id.data = session['user_id']

    if form.validate_on_submit():
        failed = False

        # check if ssn matches student ssn for verification
        if not user_service.verify_student_ssn(form.student_user_id.data, form.social_security_last_four.data):
            flash("User identification could not be confirmed.")
            failed = True

        if not failed:
            # save loan application
            if not loan_service.save_loan_application(form.student_user_id.data, form.bank_loan_offer_id.data, form.loan_amount.data, form.name.data, form.loan_term_months.data):
                flash("An error occurred while submitting the loan application.")
                failed = True
            
        # show success or failure message
        if not failed:
            flash("Loan application submitted successfully.")
            return redirect(url_for('review_bank_loan_page'))
        else:
            flash("The loan application could not be submitted.")

    return render_template("loan_application_page.html", title="Apply for a Loan", form=form, bank_loan_offer=bank_loan_offer, bank=bank)

# monthly payment calculator page
@app.route('/monthly-payment-calculator', methods=['GET', 'POST'])
@student_only
def monthly_payment_calculator_page():
    return render_template("monthly_payment_calculator_page.html", title = "Calculate your monthly payments")

# fetches all approved loans for student
# used by monthly payment calculator page
@app.route('/get-all-approved-loans-student-json', methods=['GET', 'POST'])
@student_only
def get_all_approved_loans_student_json():
    loans = loan_service.get_all_approved_loans_for_student(session['user_id'])
    loan_offers = loan_service.get_all_bank_loan_offers()

    # allows for reference to bank_loan_offer object based on loan.bank_loan_offer_id
    loan_offers_dict = {}
    for loan_offer in loan_offers:
        loan_offers_dict[loan_offer.id] = loan_offer

    # convert object to dictionary, which can be easily converted to json
    loan_dicts = []
    for loan in loans:
        loan_dict = loan.__dict__
        loan_dict['offer'] = loan_offers_dict[loan.bank_loan_offer_id].__dict__
        loan_dicts.append(loan_dict)

    # convert to json   
    json_str = json.dumps(loan_dicts, default=str)

    return json_str

"""
-----------------------
| BANK OFFICIAL PAGES |
-----------------------
"""

# demo page, accessible by bank officials
@app.route('/bank-official-page')
@bank_official_only
def bank_official_page():
    return render_template("bank_official_page.html", title="Bank Official Page")
    
# url for rejecting loans
# arguments:
#   loan_id: loan to reject (required)
@app.route('/loan-rejection-page')
@bank_official_only
def loan_rejection_page():
    # try to reject loan, print success or failure message
    if loan_service.reject_loan(request.args.get('loan_id'), datetime.now()):
        flash("Loan successfully rejected.")
    else:
        flash("An error has occurred. The loan could not be rejected.")

    return redirect(url_for("bo_pending_application_page"))
    
# url for approving loans
# arguments:
#   loan_id: loan to approve (required)
@app.route('/loan-approval-page')
@bank_official_only
def loan_approval_page():
    # try to approve loan, print success of failure message
    if loan_service.approve_loan(request.args.get('loan_id'), datetime.now()):
        flash("Loan successfully approved.") 
    else:
        flash("An error has occurred. The loan could not be approved.") 

    return redirect(url_for("bo_pending_application_page"))

# bank official loan overview page
@app.route('/bo_review_bank_loan_page')
@bank_official_only
def bo_review_bank_loan_page():
    loans = loan_service.get_all_loans_for_bank_official(session['user_id'])
    students = user_service.get_all_students()
    universities = institution_service.get_all_universities()
    loan_offers = loan_service.get_all_bank_loan_offers()

    # allows for reference to student object based on loan.student_user_id
    student_dict = {}
    for student in students:
        student_dict[student.id] = student

    # allows for reference to university object based on student.university_id
    university_dict = {}
    for university in universities:
        university_dict[university.id] = university

    # allows for reference to bank_loan_offer object based on loan.bank_loan_offer_id
    loan_offers_dict = {}
    for loan_offer in loan_offers:
        loan_offers_dict[loan_offer.id] = loan_offer
        
    return render_template("bo_review_bank_loan_page.html", title = "Review Bank Loans", loans = loans, student_dict = student_dict, university_dict = university_dict, loan_offers_dict = loan_offers_dict)

# pending loan applications to approve or reject
@app.route('/bo_pending_application_page')
@bank_official_only
def bo_pending_application_page():
    loans = loan_service.get_all_loan_applications_for_bank_official(session['user_id'])
    students = user_service.get_all_students()
    universities = institution_service.get_all_universities()
    loan_offers = loan_service.get_all_bank_loan_offers()

    # allows for reference to student object based on loan.student_user_id
    student_dict = {}
    for student in students:
        student_dict[student.id] = student

    # allows for reference to university object based on student.university_id
    university_dict = {}
    for university in universities:
        university_dict[university.id] = university

    # allows for reference to bank_loan_offer object based on loan.bank_loan_offer_id
    loan_offers_dict = {}
    for loan_offer in loan_offers:
        loan_offers_dict[loan_offer.id] = loan_offer
        
    return render_template("bo_pending_applications_page.html", title = "Pending Loan Applications", loans = loans, student_dict = student_dict, university_dict = university_dict, loan_offers_dict = loan_offers_dict)

"""
---------------------------------
| SCHOOL BILLING OFFICIAL PAGES |
---------------------------------
"""

# demo page, accessible by school billing officials
@app.route('/school-billing-official-page')
@school_billing_official_only
def school_billing_official_page():
    return render_template("school_billing_official_page.html", title="School Billing Official Page")


"""
--------------
| MISC PAGES |
--------------
"""

# access denied page
@app.route('/access-denied')
def access_denied_page():
    return render_template("access_denied.html", title="Access Denied")