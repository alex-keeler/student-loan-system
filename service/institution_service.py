from service.base_service import BaseService

class InstitutionService(BaseService):
    def __init__(self, university_dao, bank_dao):
        self.university_dao = university_dao
        self.bank_dao = bank_dao

    # gets university by id
    # arguments:
    #   university_id: id of the university (int)
    # returns: university (University)
    def get_university_by_id(self, university_id):
        return self.university_dao.get_university_by_id(university_id)

    # gets all universities
    # returns: array of universities (University[])
    def get_all_universities(self):
        return self.university_dao.get_all_universities()

    # gets bank by id
    # arguments:
    #   bank_id: id of the bank (int)
    # returns: bank (Bank)
    def get_bank_by_id(self, bank_id):
        return self.bank_dao.get_bank_by_id(bank_id)

    # gets all banks
    # returns: array of banks (Bank[])
    def get_all_banks(self):
        return self.bank_dao.get_all_banks()