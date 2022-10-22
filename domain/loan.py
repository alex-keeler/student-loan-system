class Loan(object):
    def __init__(self, id, status, bank_loan_offer_id, student_user_id, loan_amount, application_date, approval_date, name, amount_paid, loan_term_months):
        self.id = id
        self.status = status
        self.bank_loan_offer_id = bank_loan_offer_id
        self.student_user_id = student_user_id
        self.loan_amount = loan_amount
        self.application_date = application_date
        self.approval_date = approval_date
        self.name = name
        self.amount_paid = amount_paid
        self.loan_term_months = loan_term_months

"""
+--------------------+--------------+------+-----+---------+----------------+
| Field              | Type         | Null | Key | Default | Extra          |
+--------------------+--------------+------+-----+---------+----------------+
| id                 | int(11)      | NO   | PRI | NULL    | auto_increment |
| status             | varchar(45)  | NO   |     | NULL    |                |
| bank_loan_offer_id | int(11)      | NO   | MUL | NULL    |                |
| student_user_id    | int(11)      | NO   | MUL | NULL    |                |
| loan_amount        | decimal(9,2) | NO   |     | NULL    |                |
| application_date   | datetime     | YES  |     | NULL    |                |
| approval_date      | datetime     | YES  |     | NULL    |                |
| name               | varchar(255) | YES  |     | NULL    |                |
| amount_paid        | decimal(9,2) | YES  |     | NULL    |                |
| loan_term_months   | int(11)      | NO   |     | NULL    |                |
+--------------------+--------------+------+-----+---------+----------------+
"""