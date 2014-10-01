
import logging

class EditTest:
    def __init__(self, manager, UI_factory, test_manager, test_name, test_id):
        self.logprefix = "EditTest"
        logging.info("{0}:{1}:".format(self.logprefix, "__init__"))
        self.manager = manager
        self.UI_factory = UI_factory
        self.edit_test_UI = UI_factory.create_edit_test_UI()
        self.test_manager = test_manager
        self.test_name = test_name
        self.test_id = test_id

    def start(self):
        self.edit_test_UI.start(self)

    def getDeToEn(self):
        return True
    
    def getNumberOfItems(self):
        return 0

    def quit(self):
        self.manager.quit()

    def back_to_test_selection(self):
        self.manager.do_test_selection()
