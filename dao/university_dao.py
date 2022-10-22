from dao.base_dao import BaseDao
from dao.database import Database
from domain.university import University

class UniversityDao(BaseDao):
    def __init__(self, db):
        super().__init__(db)

    # fetches university by id
    # arguments:
    #   university_id: id for university (int)
    # returns: university (University)
    def get_university_by_id(self, university_id):

        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, name, address
            FROM university u
            WHERE u.id = %s
        """)
        parameters = (university_id,)
        cursor.execute(query, parameters)

        # gather results
        results = []
        for result in cursor:
            results.append(result)

        cursor.close()
        cnx.close()

        # get single result or None, convert to university object
        university_data = Database.get_first_or_none(results)
        university = University(*university_data) if university_data != None else None

        return university

    # fetches all universities
    # returns: array of universities (University[])
    def get_all_universities(self):
        
        cnx, cursor = self.db.open_connection()

        # build and execute query
        query = ("""
            SELECT id, name, address
            FROM university u
        """)
        cursor.execute(query)

        # gather results, convert to university objects
        universities = []
        for result in cursor:
            universities.append(University(*result))

        cursor.close()
        cnx.close()

        return universities