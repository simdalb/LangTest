
import logging

class TestSelection:
    def __init__(self, manager, UI_factory, test_manager, user_name, user_id, dated_score_handler):
        self.logprefix = "TestSelection"
        logging.info("{0}:{1}:".format(self.logprefix, "__init__"))
        self.manager = manager
        self.UI_factory = UI_factory
        self.test_selection_UI = UI_factory.create_test_selection_UI()
        self.test_manager = test_manager
        self.user_name = user_name
        self.user_id = user_id
        self.dated_score_handler = dated_score_handler
        
    def start(self):
        self.test_selection_UI.start(self)

    def set_test_name(self, test_name):
        test_id = self.test_manager.get_test_id(test_name)
        logging.info("{0}:{1}: test_name: {2} has test_id: {3}".format(self.logprefix, "set_test_name", test_name, test_id))
        test_exists = test_id > 0
        if test_exists:
            self.manager.do_edit_test(test_name, test_id)
        return test_exists
    
    def set_test_id(self, test_id):
        self.manager.do_edit_test(self.test_manager.get_test_name(test_id), test_id)
    
    def get_tests(self):
        test_list = self.test_manager.get_tests(self.user_id)
        test_list.sort(key=lambda(test):self.dated_score_handler.effective_score(test[3], test[4], test[2]))
        return test_list

    def inform_test_exists(self, test_name):
        self.UI_factory.create_InformTestExistsPopupWindow(self.test_selection_UI).start(test_name)
    
    def test_exists(self, test_name):
        return self.test_manager.test_exists(test_name)
        
    def receive_partial_text(self, text):
        return self.test_manager.get_matches(text)
    
    def create_test(self, test_name):
        logging.info("{0}:{1}: creating test: {2}".format(self.logprefix, "create_test", test_name))
        self.test_selection_UI.finish()
        test_id = self.test_manager.create_test(test_name, self.dated_score_handler.getNowText())
        self.manager.do_edit_test(test_name, test_id)

    def prompt_new_test(self, test_name):
        logging.info("{0}:{1}: creating test: {2}".format(self.logprefix, "prompt_new_test", test_name))
        self.UI_factory.create_CreateTestPopupWindow(self.test_selection_UI).start(test_name, self)
        
    def quit(self):
        self.manager.quit()
    
    def back_to_login(self):
        self.manager.do_login()