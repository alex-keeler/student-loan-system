from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, DateField, SelectField, IntegerField, RadioField, DecimalField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, Email, NumberRange, ValidationError
from datetime import date

from wtforms.widgets import html_params

# custom validator, requires that field date be before specified date
# arguments:
#   date: cutoff date
#   message: error message if field date is not before date
def date_before(date, message=None):
    def _date_before(form, field):
        if field.data >= date:
            raise ValidationError(message)
    
    return _date_before

# login form fields, used by wtforms.quick_form
class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

# register form fields, used by wtforms.quick_form
class RegisterUserForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    email_address = StringField("Email Address: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=8, max=30,
        message="Password must be between 8 and 30 characters")])
    password_retype = PasswordField("Retype Password: ", validators=[DataRequired(),
        EqualTo('password', message="Passwords do not match.")])
    first_name = StringField("First Name: ", validators=[DataRequired()])
    last_name = StringField("Last Name: ", validators=[DataRequired()])
    date_of_birth = DateField("Date of birth: ", validators=[DataRequired(), date_before(date.today(), message="Date must be before today.")])
    user_type = SelectField("Occupation: ", id="user_type_select", choices=[('STUDENT', 'Student'), ('BANK_OFFICIAL', 'Bank Official'), ('SCHOOL_BILLING_OFFICIAL', 'School Billing Official')], validators=[DataRequired()])
    university = SelectField("University: ", id='university_select',coerce=int,validate_choice=False)
    bank = SelectField("Bank: ", id='bank_select',coerce=int,validate_choice=False)
    organization_id = StringField("Organization ID: ", id='organization_id')
    social_security_last_four = IntegerField("Social Security # (Last Four Digits):", id='social_security_last_four', validators=[NumberRange(min=0000, max=9999)])
    submit = SubmitField("Submit")

# loan application form fields, used by wtforms.quick_form
class LoanApplicationForm(FlaskForm):
    bank_loan_offer_id = HiddenField()
    student_user_id = HiddenField()
    loan_amount = DecimalField('Loan amount (USD): ', places=2, validators=[DataRequired(), NumberRange(min=0.00, max=1000000.00)])
    loan_term_months = IntegerField("Loan term (months): ", validators=[DataRequired(), NumberRange(min=1)])
    name = StringField('Loan nickname: ')
    social_security_last_four = IntegerField("Social Security # (Last Four Digits): ", validators=[DataRequired(), NumberRange(min=0000, max=9999)])
    submit = SubmitField("Submit")