
import user_manager

class DataFactorySQL:
    def __init__(self, cursor):
        self.cursor = cursor
    
    def create_user_manager(self):
        return user_manager.UserManager(self.cursor)