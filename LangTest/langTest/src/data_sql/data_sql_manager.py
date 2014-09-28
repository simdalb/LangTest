
import sqlite3
from mysql.connector import errorcode
import data_factory_SQL
import logging

class DataSQLManager:
    def __init__(self):
        self.logprefix = "DataSQLManager"
        DB_NAME = "langtest"
        self.connect = sqlite3.connect(DB_NAME)
        self.cursor = self.connect.cursor()
        self.data_factory_SQL = data_factory_SQL.DataFactorySQL(self.cursor, self.connect)
        self.cursor.execute( \
                             "CREATE TABLE IF NOT EXISTS users " + \
                             "(" + \
                                "userId INTEGER, " + \
                                "userName CHAR(50) NOT NULL, " + \
                                "PRIMARY KEY (userId), " + \
                                "UNIQUE (userName)" + \
                             ")" \
                           )
        self.cursor.execute( \
                             "CREATE TABLE IF NOT EXISTS tests " + \
                             "(" + \
                                "testId INTEGER, " + \
                                "testName CHAR(50) NOT NULL, " + \
                                "PRIMARY KEY (testId), " + \
                                "UNIQUE (testName)" + \
                             ")" \
                           )
        self.cursor.execute( \
                             "CREATE TABLE IF NOT EXISTS testContents " + \
                             "(" + \
                                "testId INTEGER NOT NULL, " + \
                                "questionId INTEGER NOT NULL, " + \
                                "termLang1 CHAR(50) NOT NULL, " + \
                                "termLang2 CHAR(50) NOT NULL, " + \
                                "FOREIGN KEY (testId) REFERENCES tests(testId), " + \
                                "PRIMARY KEY (questionId, testId)" + \
                             ")" \
                           )
        self.cursor.execute( \
                             "CREATE TABLE IF NOT EXISTS stats " + \
                             "(" + \
                                "userId INTEGER NOT NULL, " + \
                                "testId INTEGER NOT NULL, " + \
                                "timestamp CHAR(50) NOT NULL, " + \
                                "score INTEGER NOT NULL, " + \
                                "FOREIGN KEY (userId) REFERENCES users(userId), " + \
                                "FOREIGN KEY (testId) REFERENCES tests(testId), " + \
                                "UNIQUE (timestamp)" + \
                             ")" \
                           )
        logging.info("{0}:{1}: created DB: {2}".format(self.logprefix, "__init__", DB_NAME))

    def get_data_factory(self):
        return self.data_factory_SQL
    
    def quit(self):
        logging.info("{0}:{1}: closing DB".format(self.logprefix, "quit"))
        self.connect.close()