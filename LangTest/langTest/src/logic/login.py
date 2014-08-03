
class Login:
    def __init__(self, manager, login_UI, user_manager):
        self.manager = manager
        self.login_UI = login_UI
        self.user_manager = user_manager
        self.login_UI.start(self)

    def set_user_name(self, user_name):
        user_id = self.user_manager.get_user_id(user_name)
        user_exists = user_id > 0
        if user_exists:
            self.manager.do_menu(user_name, user_id)
        return user_exists
        
    def receive_partial_text(self, text):
        return self.user_manager.get_matches(text)
    
    def create_user(self, user_name):
        self.manager.do_menu(user_name, self.user_manager.create_user(user_name))
