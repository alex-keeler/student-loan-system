import mysql.connector

class Database(object):
    def __init__(self, host="127.0.0.1", username="loanuser", password="loanuser", database="loandb"):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def open_connection(self):
        """
        Opens a new connection to the database and returns the connection and a cursor used to
        navigate the database.
        Returns: A connection to the database (mysql.connector), a cursor (mysql.connector.cursor)
        Note: Remember to close the cursor and database connection when you are done with them!
        """

        cnx = mysql.connector.connect(username=self.username, password=self.password,
            database=self.database, host=self.host, port=3306)

        return cnx, cnx.cursor()

    @staticmethod
    def get_first_or_none(results):

        if len(results) == 0:
            return None
        else:
            return tuple(results[0])