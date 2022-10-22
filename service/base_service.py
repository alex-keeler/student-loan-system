class BaseService(object):

    @staticmethod
    def sanitize(in_str):
        """
        Sanitizes and returns any string input used in an SQL Query to prevent SQL Injection
        in_str: The string to be sanitized (str)
        Returns: The sanitized string (str)
        """

        out_str = ""

        for char in in_str:
            if char == "'" or char == '"':
                out_str += "\\" + char
            else:
                out_str += char

        return out_str