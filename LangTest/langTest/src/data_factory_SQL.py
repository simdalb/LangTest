
from data_sql import user_manager

class DataFactorySQL:
    def __init__(self):
        pass
    
    def create_user_manager(self):
        return user_manager.UserManager()