
import logging

class UserManager:
    def __init__(self, cursor, connect):
        self.logprefix = "UserManager"
        self.cursor = cursor
        self.connect = connect
    
    def get_user_id(self, user_name):
        self.cursor.execute("SELECT userId FROM users WHERE userName = '" + user_name + "'")
        userId = -1
        row = self.cursor.fetchone()
        if row != None:
            userId = row[0]
        logging.info("{0}:{1}: user name: {2} has user id: {3}".format(self.logprefix, "get_user_id", user_name, userId))
        return userId
    
    def get_users(self):
        self.cursor.execute("SELECT userName FROM users")
        user_name_list = []
        for (user_name,) in self.cursor.fetchall():
            logging.info("{0}:{1}: found user name: {2} in DB".format(self.logprefix, "get_users", user_name))
            user_name_list.append(user_name)
        return user_name_list
    
    def user_exists(self, user_name):
        logging.info("{0}:{1}: checking if user name: {2} exists".format(self.logprefix, "user_exists", user_name))
        return self.get_user_id(user_name) != -1

    def get_matches(self, text):
        logging.info("{0}:{1}: searching for user names that match text: {2}".format(self.logprefix, "get_matches", text))
        self.cursor.execute("SELECT userName FROM users WHERE userName LIKE '" + text + "'")
        user_name_list = []
        for (user_name,) in self.cursor.fetchall():
            logging.info("{0}:{1}: user name: {2} matches text".format(self.logprefix, "get_matches", user_name))
            user_name_list.append(user_name)
        return user_name_list

    def create_user(self, user_name):
        logging.info("{0}:{1}: creating user name: {2}".format(self.logprefix, "create_user", user_name))
        self.cursor.execute("INSERT INTO users (userName) VALUES ('" + user_name + "')")
        self.cursor.execute("INSERT INTO userPersistency VALUES ('" + str(self.get_user_id(user_name)) + "', '1')")
        logging.info("{0}:{1}: insertion done".format(self.logprefix, "create_user"))
        self.connect.commit()
        return self.get_user_id(user_name)
    