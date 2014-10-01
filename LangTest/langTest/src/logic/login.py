
import logging

class Login:
    def __init__(self, manager, UI_factory, user_manager):
        self.logprefix = "Login"
        logging.info("{0}:{1}:".format(self.logprefix, "__init__"))
        self.manager = manager
        self.UI_factory = UI_factory
        self.login_UI = UI_factory.create_login_UI()
        self.user_manager = user_manager
        
    def start(self):
        self.login_UI.start(self)

    def set_user_name(self, user_name):
        user_id = self.user_manager.get_user_id(user_name)
        logging.info("{0}:{1}: user_name: {2} has user_id: {3}".format(self.logprefix, "set_user_name", user_name, user_id))
        user_exists = user_id > 0
        if user_exists:
            self.manager.do_test_selection(user_name, user_id)
        return user_exists
    
    def get_users(self):
        return self.user_manager.get_users()
    
    def inform_user_exists(self, user_name):
        self.UI_factory.create_InformUserExistsPopupWindow(self.login_UI).start(user_name)
    
    def user_exists(self, user_name):
        return self.user_manager.user_exists(user_name)
        
    def receive_partial_text(self, text):
        return self.user_manager.get_matches(text)
    
    def create_user(self, user_name):
        logging.info("{0}:{1}: creating user name: {2}".format(self.logprefix, "create_user", user_name))
        user_id = self.user_manager.create_user(user_name)
        self.login_UI.finish()
        self.manager.do_test_selection(user_name, user_id)

    def prompt_new_user(self, user_name):
        logging.info("{0}:{1}: creating user name: {2}".format(self.logprefix, "prompt_new_user", user_name))
        self.UI_factory.create_CreateUserPopupWindow(self.login_UI).start(user_name, self)

    def quit(self):
        self.manager.quit()
