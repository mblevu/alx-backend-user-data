#!/usr/bin/env python3
"""regex-ing """
import re
from typing import List, Tuple
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialize"""
        super(RedactingFormatter, self).__init__(
            "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
        )
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(rf"{field}=.+?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """takes no arguments and returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(sh)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )


def main():
    """takes no arguments and returns nothing"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    [print(user) for user in cursor]
