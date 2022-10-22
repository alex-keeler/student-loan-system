from re import L
from domain.user import User
from domain.enum.user_type import UserType

class Student(User):
    def __init__(self, id, username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, credit_score, social_security_last_four, university_id):
        super().__init__(id, username, password_hash, email_address, first_name, last_name, organization_id, date_of_birth, UserType.STUDENT)
        self.credit_score = credit_score
        self.social_security_last_four = social_security_last_four
        self.university_id = university_id

"""
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| id              | int(11)      | NO   | PRI | NULL    | auto_increment |
| organization_id | varchar(45)  | YES  |     | NULL    |                |
| first_name      | varchar(100) | NO   |     | NULL    |                |
| last_name       | varchar(100) | NO   |     | NULL    |                |
| email_address   | varchar(100) | NO   | UNI | NULL    |                |
| username        | varchar(100) | NO   | UNI | NULL    |                |
| password_hash   | varchar(255) | NO   |     | NULL    |                |
| date_of_birth   | date         | NO   |     | NULL    |                |
| user_type       | varchar(45)  | NO   |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+

+---------------------------+---------+------+-----+---------+-------+
| Field                     | Type    | Null | Key | Default | Extra |
+---------------------------+---------+------+-----+---------+-------+
| user_id                   | int(11) | NO   | PRI | NULL    |       |
| credit_score              | int(11) | YES  |     | NULL    |       |
| social_security_last_four | int(11) | NO   |     | NULL    |       |
| university_id             | int(11) | NO   | MUL | NULL    |       |
+---------------------------+---------+------+-----+---------+-------+
"""