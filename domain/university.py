class University(object):
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

"""
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| id      | int(11)      | NO   | PRI | NULL    | auto_increment |
| name    | varchar(100) | NO   | UNI | NULL    |                |
| address | varchar(255) | NO   |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+
"""