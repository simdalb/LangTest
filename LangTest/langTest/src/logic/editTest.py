
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
        self.edit_test_UI.clearAppendText()

    def inform_item_exists(self, found_test_name, firstAppendTextValue, secondAppendTextValue):
        self.UI_factory.create_InformItemExistsPopupWindow(self.edit_test_UI).start(found_test_name, 
                                                                                    self.test_name, 
                                                                                    firstAppendTextValue, 
                                                                                    secondAppendTextValue)
        
    def select_other_test(self, ret_list):
        self.UI_factory.create_SelectOtherTestPopupWindow(self.edit_test_UI).start(ret_list, self)
        
    def inform_no_empty_fields(self):
        self.UI_factory.create_InformNoEmptyFieldsPopupWindow(self.edit_test_UI).start()
        
    def prompt_delete_test(self):
        self.UI_factory.create_PromptDeleteTestPopupWindow(self.edit_test_UI).start(self.test_name, self)
        
    def delete_test(self):
        self.test_manager.delete_test(self.test_id)
        
    def import_test(self):
        return self.UI_factory.getPathFromImportFileDialog(self.edit_test_UI)

    def parse_file(self, path):
        input_file = open(path, "r")
        termsList = []
        for line in input_file:
            if(line[-1] == "\n"):
                line = line[:-1]
            terms = line.split("|")
            if(len(terms) != 2):
                input_file.close()
                return (-1, len(termsList) + 1)
            terms[0] = terms[0].strip()
            terms[1] = terms[1].strip()
            logging.info("{0}:{1}: left term: {2}, right term: {3}".format(self.logprefix, "parse_file", terms[0], terms[1]))
            termsList.append(terms)    
        input_file.close()
        for terms in termsList:
            self.edit_test_UI.process_ret_list(self.append_item(terms[0], terms[1]))
        return (0, 0)
    
    def quit(self):
        self.manager.quit()

    def back_to_test_selection(self):
        self.manager.do_test_selection(self.user_name, self.user_id)
