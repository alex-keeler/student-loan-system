# student data access object
from dao.base_dao import BaseDao
from dao.database import Database
from domain.student import Student

class StudentDao(BaseDao):
    def __init__(self, db):
        super().__init__(db)

    # creates a new student entry
    # arguments:   
    #   user_id: user id (int)
    #   credit_score: credit score (int or None)
    #   social_security_last_four: last four digits of social security number (int)
    #   university_id: university id (int)
    def register_student(self, user_id, credit_score, social_security_last_four, university_id):
        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            INSERT INTO student
            (user_id, credit_score, social_security_last_four, university_id)
            VALUES (%s, %s, %s, %s)
             """)
        parameters = (user_id, credit_score, social_security_last_four, university_id)
        cursor.execute(query, parameters)

        # commit change
        cnx.commit()

        cursor.close()
        cnx.close()

    # fetches student by user id
    # arguments:
    #   user_id: user id for student (int)
    # returns: student (Student)
    def get_by_user_id(self, user_id):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT u.id, u.username, u.password_hash, u.email_address, u.first_name, u.last_name, u.organization_id, u.date_of_birth, s.credit_score, s.social_security_last_four, s.university_id
            FROM student s
            JOIN users u ON s.user_id = u.id
            WHERE s.user_id = %s
        """)
        parameters = (user_id,)
        cursor.execute(query, parameters)

        # gather results
        results = []
        for result in cursor:
            results.append(result)

        cursor.close()
        cnx.close()

        # get single result or None, convert to student object
        student_data = Database.get_first_or_none(results)
        student = Student(*student_data) if student_data is not None else None

        return student

    # fetches all students
    # returns: array of students (Student[])
    def get_all_students(self):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT u.id, u.username, u.password_hash, u.email_address, u.first_name, u.last_name, u.organization_id, u.date_of_birth, s.credit_score, s.social_security_last_four, s.university_id
            FROM student s
            JOIN users u ON s.user_id = u.id
        """)
        cursor.execute(query)

        # gather result, convert to student objects
        students = []
        for result in cursor:
            students.append(Student(*result))

        cursor.close()
        cnx.close()

        return students