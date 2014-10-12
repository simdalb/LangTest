
import logging
from common import found_status
from common import item_list_bounds_status

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
        self.testList = []
        self.itemNumber = -1
        self.questionId = -1

    def start(self):
        self.edit_test_UI.start(self)

    def getDeToEn(self):
        return self.persistency_manager.getDeToEn(self.user_id)
    
    def getUserName(self):
        return self.user_name
    
    def getTestName(self):
        return self.test_name
    
    def getNumberOfItems(self):
        return self.test_manager.getNumberOfItems(self.test_id)
    
    def isNotFirstItem(self):
        logging.info("{0}:{1}: current item number: {2}".format(self.logprefix, "isNotFirstItem", self.itemNumber))
        return self.itemNumber > 1

    def switchDeToEn(self):
        if self.getDeToEn():
            logging.info("{0}:{1}: DeToEn: {2}".format(self.logprefix, "switchDeToEn", "True->False"))
            self.persistency_manager.setDeToEn(False, self.user_id)
        else:
            logging.info("{0}:{1}: DeToEn: {2}".format(self.logprefix, "switchDeToEn", "False->True"))
            self.persistency_manager.setDeToEn(True, self.user_id)

    def append_item(self, firstAppendTextValue, secondAppendTextValue):
        if self.itemNumber == -1:
            self.itemNumber = 0
        if self.getDeToEn():
            logging.info("{0}:{1}: appending de to en".format(self.logprefix, "append_item"))
            ret_list = self.test_manager.append_item(self.test_id, firstAppendTextValue, secondAppendTextValue)
            if ret_list[0][0] == found_status.FoundStatus.NONE_FOUND:
                self.testList.append([self.test_manager.get_question_id(firstAppendTextValue, secondAppendTextValue), 
                                      firstAppendTextValue, secondAppendTextValue])
            return ret_list
        else:
            logging.info("{0}:{1}: appending en to de".format(self.logprefix, "append_item"))
            ret_list = self.test_manager.append_item(self.test_id, secondAppendTextValue, firstAppendTextValue)
            if ret_list[0][0] == found_status.FoundStatus.NONE_FOUND:
                self.testList.append([self.test_manager.get_question_id(secondAppendTextValue, firstAppendTextValue), 
                                      secondAppendTextValue, firstAppendTextValue])
            return ret_list
        
    def modify_question(self, firstTextValue, secondTextValue):
        if self.getDeToEn():
            ret_list = self.test_manager.modify_question(self.test_id, self.questionId, firstTextValue, secondTextValue)
            if ret_list[0][0] == found_status.FoundStatus.NONE_FOUND:
                self.testList[self.itemNumber - 1] = (self.questionId, firstTextValue, secondTextValue)
        else:
            self.test_manager.modify_question(self.test_id, self.questionId, secondTextValue, firstTextValue)
            if ret_list[0][0] == found_status.FoundStatus.NONE_FOUND:
                self.testList[self.itemNumber - 1] = (self.questionId, secondTextValue, firstTextValue)
        return ret_list

    def append_item_to_other_test(self, test_name, german_value, english_value):
        logging.info("{0}:{1}: appending".format(self.logprefix, "append_item_to_other_test"))
        self.test_manager.append_item_to_other_test(test_name, german_value, english_value)
        self.edit_test_UI.clearAppendText()
        
    def delete_current_item(self):
        logging.info("{0}:{1}: deleting item number {2}".format(self.logprefix, "delete_current_item", self.itemNumber))
        self.test_manager.delete_item(self.questionId)
        self.testList.pop(self.itemNumber - 1)
        if len(self.testList) == self.itemNumber - 1:
            self.itemNumber -= 1
        theItemListBoundsStatus = item_list_bounds_status.ItemListBoundsStatus.NEITHER
        if len(self.testList) == 0:
            theItemListBoundsStatus = item_list_bounds_status.ItemListBoundsStatus.EMPTY
        elif len(self.testList) == 1:
            theItemListBoundsStatus = item_list_bounds_status.ItemListBoundsStatus.BOTH
            self.itemNumber = 1
        elif len(self.testList) == self.itemNumber:
            theItemListBoundsStatus = item_list_bounds_status.ItemListBoundsStatus.END
        elif self.itemNumber == 1:
            theItemListBoundsStatus = item_list_bounds_status.ItemListBoundsStatus.BEGIN
        else:
            logging.error("{0}:{1}: error, unexpected use case".format(self.logprefix, "delete_current_item"))
        self.edit_test_UI.setNewEditTextAfterDelete(theItemListBoundsStatus)
        
    def getCurrentItem(self):
        (self.questionId, itemFirst, itemSecond) = self.testList[self.itemNumber - 1]
        item = []
        if self.getDeToEn():
            item.append(itemFirst)
            item.append(itemSecond)
        else:
            item.append(itemSecond)
            item.append(itemFirst)
        return item

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
        self.edit_test_UI.goBackToTestSelection()
        
    def import_test(self):
        return self.UI_factory.getPathForImportFileDialog(self.edit_test_UI)
    
    def export_test(self):
        return self.UI_factory.getPathForExportFileDialog(self.edit_test_UI)
    
    def write_to_file(self, path):
        output_file = open(path, "w")
        items = self.test_manager.getAllItems(self.test_id)
        for item in items:
            if self.getDeToEn():
                output_file.write(item[0] + " | " + item[1] + "\n")
            else:
                output_file.write(item[1] + " | " + item[0] + "\n")
        output_file.close()
        
    def getItemNumber(self):
        return self.itemNumber
        
    def setTestList(self):
        if not self.testList:
            logging.info("{0}:{1}: initializing testList".format(self.logprefix, "getNextItem"))
            self.testList = self.test_manager.getTestList(self.test_id)
            self.itemNumber = 0
        
    def getNextItem(self):
        logging.info("{0}:{1}: testList size: {2}".format(self.logprefix, "getNextItem", len(self.testList)))
        self.setTestList()
        if self.itemNumber < len(self.testList):
            (self.questionId, itemFirst, itemSecond) = self.testList[self.itemNumber]
            logging.info("{0}:{1}: list length: {2}, returning questionId: {3}, itemNumber: {4}".format(self.logprefix, 
                                                                                                        "getNextItem", 
                                                                                                        len(self.testList),
                                                                                                        self.questionId, 
                                                                                                        self.itemNumber))
            self.itemNumber += 1
            is_end = False
            if self.itemNumber == len(self.testList):
                is_end = True
            if self.getDeToEn():
                logging.info("{0}:{1}: returning {2}, {3}".format(self.logprefix, "getNextItem", itemFirst, itemSecond))
                return (is_end, itemFirst, itemSecond)
            else:
                logging.info("{0}:{1}: returning {2}, {3}".format(self.logprefix, "getNextItem", itemSecond, itemFirst))
                return (is_end, itemSecond, itemFirst)
        else:
            logging.info("{0}:{1}: error, end of list already reached".format(self.logprefix, "getNextItem"))
            return None

    def getPreviousItem(self):
        self.itemNumber -= 1
        (self.questionId, itemFirst, itemSecond) = self.testList[self.itemNumber - 1]
        if self.getDeToEn():
            logging.info("{0}:{1}: returning {2}, {3}".format(self.logprefix, "getPreviousItem", itemFirst, itemSecond))
            return (itemFirst, itemSecond)
        else:
            logging.info("{0}:{1}: returning {2}, {3}".format(self.logprefix, "getPreviousItem", itemSecond, itemFirst))
            return (itemSecond, itemFirst)
        
    def searchExpression(self, expr):
        matches = self.test_manager.getMatches(expr, self.test_id)
        logging.info("{0}:{1}: found {2} items for expression: {3}".format(self.logprefix, "searchExpression", len(matches), expr))
        if not self.getDeToEn():
            for item in matches:
                item1 = ''.join(item[1])
                item[1] = ''.join(item[2])
                item[2] = item1
        self.UI_factory.create_SelectItemPopupWindow(self.edit_test_UI).start(matches, self)
        
    def set_question(self, questionId):
        self.setTestList()
        self.itemNumber = 1
        logging.info("{0}:{1}: searching for questionId: {2}".format(self.logprefix, "set_question", questionId))
        while not questionId == self.testList[self.itemNumber - 1][0]:
            logging.info("{0}:{1}: questionId: {2}".format(self.logprefix, "set_question", self.testList[self.itemNumber - 1][0]))
            self.itemNumber += 1
        (self.questionId, itemFirst, itemSecond) = self.testList[self.itemNumber - 1]
        is_end = False
        if self.itemNumber == len(self.testList):
            is_end = True
        if self.getDeToEn():
            logging.info("{0}:{1}: returning {2}, {3}".format(self.logprefix, "set_question", itemFirst, itemSecond))
            self.edit_test_UI.set_item(is_end, itemFirst, itemSecond)
        else:
            logging.info("{0}:{1}: returning {2}, {3}".format(self.logprefix, "set_question", itemSecond, itemFirst))
            self.edit_test_UI.set_item(is_end, itemSecond, itemFirst)

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
            if self.getDeToEn():
                terms[0] = terms[0].strip()
                terms[1] = terms[1].strip()
            else:
                terms0 = terms[0].strip()
                terms[0] = terms[1].strip()
                terms[1] = terms0
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
