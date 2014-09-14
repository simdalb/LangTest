
from logic import login
import logging

logging.getLogger().setLevel(logging.INFO)

class Manager:
    def __init__(self, UI_factory, data_manager):
        self.logprefix = "Manager"
        logging.info("{0}:{1}: start".format(self.logprefix, "__init__"))
        self.data_manager = data_manager
        self.login = login.Login(self, UI_factory, data_manager.get_data_factory().get_user_manager())
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
        logging.info("{0}:{1}: logged on as user: {2} with Id: {3}".format(self.logprefix, "do_menu", user_name, user_id))
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
        
    def quit(self):
        self.data_manager.quit()