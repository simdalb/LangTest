
from logic import login 

class Manager:
    def __init__(self, UI_factory, data_factory):
        self.login = login.Login(self, UI_factory.create_login_UI(), data_factory.create_user_manager())
        """
        start = Start(self)
        preview = Preview(self)
        test = Test(self)
        create_test = CreateTest(self)
        statistics = Statistics(self)
        """
    def do_login(self):
        self.login.start()
        
    def do_menu(self, user_name, user_id):
        pass
        
        """
    def do_start():
        start.run()
        
    def do_preview():
        preview.run()
        
    def do_test():
        test.run()
        
    def do_create_test():
        create_test.run()
        
    def do_statistics():
        statistics.run()
        """