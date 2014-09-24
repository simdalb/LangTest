
import user_manager
import test_manager

class DataFactorySQL:
    def __init__(self, cursor, connect):
        self.user_manager = user_manager.UserManager(cursor, connect)
        self.test_manager = test_manager.TestManager(cursor, connect)
    
    def get_user_manager(self):
        return self.user_manager
    
    def get_test_manager(self):
        return self.test_manager