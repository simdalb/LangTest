
class UserManager:
    def __init__(self, cursor):
        self.cursor = cursor
    
    def get_user_id(self, user_name):
        self.cursor.execute("SELECT userId FROM users WHERE userName = '" + user_name + "'")
        userId = -1
        row = self.cursor.fetchone()
        if row != None:
            userId = row[0]
        return userId

    def get_matches(self, text):
        self.cursor.execute("SELECT userName FROM users WHERE userName LIKE '" + text + "'")
        user_name_list = []
        for (user_name,) in self.cursor.fetchall():
            user_name_list.append(user_name)
        return user_name_list

    def create_user(self, user_name):
        self.cursor.execute("INSERT INTO users (userName) VALUES ('" + user_name + "')")
        return self.get_user_id(user_name)