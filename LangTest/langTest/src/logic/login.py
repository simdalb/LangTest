
class Login:
    def __init__(self, manager, login_UI, user_manager):
        self.manager = manager
        self.login_UI = login_UI
        self.user_manager = user_manager
        
    def start(self):
        self.login_UI.start()
        
    def receive_username(self, user_name):
        user_id = self.user_manager.get_user_id(user_name)
        if user_id == 0:
            self.login_UI.ask_if_new_user(user_name)
        else:
            self.__finish(user_name, user_id)
            
    def receive_new_username(self, user_name):
        self.__finish(user_name, self.user_manager.set_new_user(user_name))
        
    def __finish(self, user_name, user_id):
        self.login_UI.close()
        self.manager.do_menu(user_name, user_id)