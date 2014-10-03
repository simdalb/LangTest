
import logging

class EditTest:
    def __init__(self, manager, UI_factory, test_manager, persistency_manager, user_name, user_id, test_name, test_id):
        self.logprefix = "EditTest"
        logging.info("{0}:{1}:".format(self.logprefix, "__init__"))
        self.manager = manager
        self.UI_factory = UI_factory
        self.edit_test_UI = UI_factory.create_edit_test_UI()
        self.test_manager = test_manager
        self.persistency_manager = persistency_manager
        self.user_name = user_name
        self.user_id = user_id
        self.test_name = test_name
        self.test_id = test_id

    def start(self):
        self.edit_test_UI.start(self)

    def getDeToEn(self):
        return self.persistency_manager.getDeToEn(self.user_id)
    
    def getNumberOfItems(self):
        return self.test_manager.getNumberOfItems(self.test_id)

    def switchDeToEn(self):
        if self.getDeToEn():
            logging.info("{0}:{1}: DeToEn: {2}".format(self.logprefix, "switchDeToEn", "True->False"))
            self.persistency_manager.setDeToEn(False, self.user_id)
        else:
            logging.info("{0}:{1}: DeToEn: {2}".format(self.logprefix, "switchDeToEn", "False->True"))
            self.persistency_manager.setDeToEn(True, self.user_id)

    def quit(self):
        self.manager.quit()

    def back_to_test_selection(self):
        self.manager.do_test_selection(self.user_name, self.user_id)
