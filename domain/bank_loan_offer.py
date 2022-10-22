class BankLoanOffer(object):
    def __init__(self, id, interest_rate, bank_id, interest_type, start_date, expiration_date, title):
        self.id = id
        self.interest_rate = interest_rate
        self.bank_id = bank_id
        self.interest_type = interest_type
        self.start_date = start_date
        self.expiration_date = expiration_date
        self.title = title

"""
+-----------------+--------------+------+-----+---------+-------+
| Field           | Type         | Null | Key | Default | Extra |
+-----------------+--------------+------+-----+---------+-------+
| id              | int(11)      | NO   | PRI | NULL    |       |
| interest_rate   | decimal(7,4) | NO   |     | NULL    |       |
| bank_id         | int(11)      | NO   | MUL | NULL    |       |
| interest_type   | varchar(45)  | NO   |     | NULL    |       |
| start_date      | datetime     | YES  |     | NULL    |       |
| expiration_date | datetime     | YES  |     | NULL    |       |
| title           | varchar(255) | YES  |     | NULL    |       |
+-----------------+--------------+------+-----+---------+-------+
"""