
class Login:
    def __init__(self, manager, UI_factory, user_manager):
        self.manager = manager
        self.UI_factory = UI_factory
        self.login_UI = UI_factory.create_login_UI()
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

    def prompt_new_user(self, user_name):
        self.createUserPopupWindow = self.UI_factory.create_CreateUserPopupWindow(self.login_UI)
        self.createUserPopupWindow.start(user_name, self)