
import user_manager

class DataFactorySQL:
    def __init__(self, cursor):
        self.user_manager = user_manager.UserManager(cursor)
    
    def get_user_manager(self):
        return self.user_manager