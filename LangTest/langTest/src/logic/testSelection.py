
import logging

class TestSelection:
    def __init__(self, manager, UI_factory, test_manager):
        self.logprefix = "TestSelection"
        logging.info("{0}:{1}:".format(self.logprefix, "__init__"))
        self.manager = manager
        self.UI_factory = UI_factory
        self.test_selection_UI = UI_factory.create_test_selection_UI()
        self.test_manager = test_manager
        
    def start(self):
        self.test_selection_UI.start(self)

    def set_test_name(self, test_name):
        test_id = self.test_manager.get_test_id(test_name)
        logging.info("{0}:{1}: test_name: {2} has test_id: {3}".format(self.logprefix, "set_test_name", test_name, test_id))
        test_exists = test_id > 0
        if test_exists:
            self.manager.do_test(test_name, test_id)
        return test_exists
    
    def get_tests(self):
        return self.test_manager.get_tests()
    
    def inform_test_exists(self, test_name):
        self.UI_factory.create_InformTestExistsPopupWindow(self.test_selection_UI).start(test_name)
    
    def test_exists(self, test_name):
        return self.test_manager.test_exists(test_name)
        
    def receive_partial_text(self, text):
        return self.test_manager.get_matches(text)
    
    def create_test(self, test_name):
        logging.info("{0}:{1}: creating test: {2}".format(self.logprefix, "create_test", test_name))
        self.test_selection_UI.finish()
        test_id = self.test_manager.create_test(test_name)
        self.manager.do_create_test(test_name, test_id)

    def prompt_new_test(self, test_name):
        logging.info("{0}:{1}: creating test: {2}".format(self.logprefix, "prompt_new_test", test_name))
        self.UI_factory.create_CreateTestPopupWindow(self.test_selection_UI).start(test_name, self)
        
    def quit(self):
        self.manager.quit()
    
    def back_to_login(self):
        self.manager.do_login()