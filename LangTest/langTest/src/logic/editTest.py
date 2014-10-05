
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

    def append_item(self, firstAppendTextValue, secondAppendTextValue):
        if self.getDeToEn():
            logging.info("{0}:{1}: appending de to en".format(self.logprefix, "append_item"))
            return self.test_manager.append_item(self.test_id, firstAppendTextValue, secondAppendTextValue)
        else:
            logging.info("{0}:{1}: appending en to de".format(self.logprefix, "append_item"))
            return self.test_manager.append_item(self.test_id, secondAppendTextValue, firstAppendTextValue)

    def append_item_to_other_test(self, test_name, german_value, english_value):
        logging.info("{0}:{1}: appending".format(self.logprefix, "append_item_to_other_test"))
        self.test_manager.append_item_to_other_test(test_name, german_value, english_value)

    def inform_item_exists(self, found_test_name):
        self.UI_factory.create_InformItemExistsPopupWindow(self.edit_test_UI).start(found_test_name, self.test_name)
        
    def select_other_test(self, ret_list):
        self.UI_factory.create_SelectOtherTestPopupWindow(self.edit_test_UI).start(ret_list)
        
    def inform_no_empty_fields(self):
        self.UI_factory.create_InformNoEmptyFieldsPopupWindow(self.edit_test_UI).start()

    def quit(self):
        self.manager.quit()

    def back_to_test_selection(self):
        self.manager.do_test_selection(self.user_name, self.user_id)
