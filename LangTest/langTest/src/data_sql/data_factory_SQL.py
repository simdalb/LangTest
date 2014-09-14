
import user_manager

class DataFactorySQL:
    def __init__(self, cursor, connect):
        self.user_manager = user_manager.UserManager(cursor, connect)
    
    def get_user_manager(self):
        return self.user_manager