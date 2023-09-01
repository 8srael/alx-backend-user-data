#!/usr/bin/env python3

"""Task 0. Regex-ing"""


import re
from typing import List
import logging
import os
import mysql.connector

"""Fields from user_data.csv considered as
   PII (personally identifiable information)
"""
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connects to the MySQL database
       using mysql.connector module
    """
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(user=db_user,
                                   port=3306,
                                   password=password,
                                   host=host,
                                   database=db_name)

                             
class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields or []

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def main():
    """ Display each db row under a filtered format """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = (
            "name={}; email={}; phone={}; ssn={};password={};"
            "ip={};last_login={};user_agent={};"
        ).format(
            row[0], row[1], row[2], row[3],
            row[4], row[5], row[6], row[7]
        )
        log_record = logging.LogRecord(
            "user_data",
            logging.INFO,
            None,
            None,
            message,
            None,
            None
        )
        formatter = RedactingFormatter(fields=PII_FIELDS)
        print(formatter.format(log_record))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
