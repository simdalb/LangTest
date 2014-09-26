
import mysql.connector
from mysql.connector import errorcode
import data_factory_SQL
import logging

class DataSQLManager:
    def __init__(self):
        self.logprefix = "DataSQLManager"
        user = 'root'
        host = 'localhost'
        self.connector = mysql.connector
        self.connect = self.connector.connect(user=user, host=host)

        DB_NAME = "langtest"
        self.cursor = self.connect.cursor(buffered=True)
        self.data_factory_SQL = data_factory_SQL.DataFactorySQL(self.cursor, self.connect)
        self.cursor.execute("GRANT ALL PRIVILEGES ON {0}.* TO {1}@{2} WITH GRANT OPTION".format(DB_NAME, user, host))
        self.cursor.execute("FLUSH PRIVILEGES")
        self.cursor.execute("DROP DATABASE {0}".format(DB_NAME))
        try:
            self.cursor.execute("GRANT ALL PRIVILEGES ON {0}.* TO {1}@{2} WITH GRANT OPTION".format(DB_NAME, user, host))
            self.cursor.execute("FLUSH PRIVILEGES")
            self.cursor.execute("CREATE DATABASE {0}".format(DB_NAME))
            self.cursor.execute("USE {0}".format(DB_NAME))
            self.cursor.execute( \
                                 "CREATE TABLE users " + \
                                 "(" + \
                                    "userId int(12) NOT NULL AUTO_INCREMENT, " + \
                                    "userName varchar(255) NOT NULL, " + \
                                    "PRIMARY KEY (userId), " + \
                                    "UNIQUE (userName)" + \
                                 ")" \
                               )
            self.cursor.execute( \
                                 "CREATE TABLE tests " + \
                                 "(" + \
                                    "testId int(12) NOT NULL AUTO_INCREMENT, " + \
                                    "testName varchar(255) NOT NULL, " + \
                                    "PRIMARY KEY (testId), " + \
                                    "UNIQUE (testName)" + \
                                 ")" \
                               )
            self.cursor.execute( \
                                 "CREATE TABLE testContents " + \
                                 "(" + \
                                    "testId int(12) NOT NULL, " + \
                                    "questionId int(12) NOT NULL AUTO_INCREMENT, " + \
                                    "termLang1 varchar(255) NOT NULL, " + \
                                    "termLang2 varchar(255) NOT NULL, " + \
                                    "FOREIGN KEY (testId) REFERENCES tests(testId), " + \
                                    "PRIMARY KEY (questionId, testId)" + \
                                 ")" \
                               )
            self.cursor.execute( \
                                 "CREATE TABLE stats " + \
                                 "(" + \
                                    "userId int(12) NOT NULL, " + \
                                    "testId int(12) NOT NULL, " + \
                                    "timestamp varchar(255) NOT NULL, " + \
                                    "score int(12) NOT NULL, " + \
                                    "FOREIGN KEY (userId) REFERENCES users(userId), " + \
                                    "FOREIGN KEY (testId) REFERENCES tests(testId), " + \
                                    "UNIQUE (timestamp)" + \
                                 ")" \
                               )
            logging.info("{0}:{1}: created DB: {2}".format(self.logprefix, "__init__", DB_NAME))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                logging.info("{0}:{1}: DB: {2} exists, using it".format(self.logprefix, "__init__", DB_NAME))
                self.cursor.execute("USE {0}".format(DB_NAME))
            else:
                logging.info("{0}:{1}: unexpected error: {2} when creating DB: {3}".format(self.logprefix, "__init__", err.errno, DB_NAME))

    def get_data_factory(self):
        return self.data_factory_SQL
    
    def quit(self):
        logging.info("{0}:{1}: closing DB".format(self.logprefix, "quit"))
        self.connect.close()