
import logging
import random

class Test:
    def __init__(self, manager, UI_factory, test_manager, persistency_manager, user_name, user_id, test_name, test_id, dated_score_handler):
        self.logprefix = "TestSelection"
        logging.info("{0}:{1}:".format(self.logprefix, "__init__"))
        self.manager = manager
        self.UI_factory = UI_factory
        self.test_UI = UI_factory.create_test_UI()
        self.test_manager = test_manager
        self.persistency_manager = persistency_manager
        self.user_name = user_name
        self.user_id = user_id
        self.test_name = test_name
        self.test_id = test_id
        self.dated_score_handler = dated_score_handler
        self.test_list = []
        self.wrong_results = []
        self.itemNumber = -1
        self.questionId = -1
        self.question = ""
        self.answer = ""
        self.score = 0
        self.multi_answer_list = dict()
        self.save_score = False
        
    def start(self):
        self.test_UI.start(self)
        
    def setTestList(self):
        if not self.testList:
            logging.info("{0}:{1}: initializing testList".format(self.logprefix, "getNextItem"))
            self.testList = self.test_manager.getTestList(self.test_id)
            self.itemNumber = 0
            
    def getTestName(self):
        return self.test_name
    
    def getUserName(self):
        return self.user_name
    
    def getNumberOfItems(self):
        return self.test_manager.getNumberOfItems(self.test_id)
        
    def getDeToEn(self):
        return self.persistency_manager.getDeToEn(self.user_id)

    def getNextQuestion(self):
        if not self.test_list:
            self.test_list = self.test_manager.getTestList(self.test_id)
            random.seed()
            random.shuffle(self.test_list)
        self.itemNumber += 1
        if self.getDeToEn():
            (self.questionId, self.question, self.answer) = self.test_list[self.itemNumber]
        else:
            (self.questionId, self.answer, self.question) = self.test_list[self.itemNumber]
        logging.info("{0}:{1}: question: {2}, answer: {3}".format(self.logprefix, "getNextQuestion", self.question, self.answer))
        previous_answers = []
        try:
            previous_answers = self.multi_answer_list[self.question]
        except:
            pass
        return (self.question, previous_answers)

    def getAnswer(self):
        return self.answer

    def wrong_items(self):
        return self.wrong_results

    def test_summary(self):
        self.UI_factory.create_TestSummaryPopupWindow(self.test_UI).start(self.score, self.getNumberOfItems(), self)

    def edit_previous_item(self):
        question = ""
        answer = ""
        questionId = self.test_list[self.itemNumber - 1][0]
        if self.getDeToEn():
            question = self.test_list[self.itemNumber - 1][1]
            answer = self.test_list[self.itemNumber - 1][2]
        else:
            question = self.test_list[self.itemNumber - 1][2]
            answer = self.test_list[self.itemNumber - 1][1]
        self.UI_factory.create_EditPreviousPopupWindow(self.test_UI).start(questionId, question, answer, self)

    def modify_question(self, questionId, firstTextValue, secondTextValue):
        if self.getDeToEn():
            ret_list = self.test_manager.modify_question(self.test_id, questionId, firstTextValue, secondTextValue)
        else:
            ret_list = self.test_manager.modify_question(self.test_id, questionId, secondTextValue, firstTextValue)
        return ret_list
    
    def inform_modify_later(self, ret_list, the_found_status):
        self.UI_factory.create_InformModifyLaterPopupWindow(self.test_UI).start(ret_list, the_found_status)
        
    def inform_no_score_saved(self):
        self.UI_factory.create_InformNoScoreSavedPopupWindow(self.test_UI).start()

    def receive_updated_item(self, question, answer):
        self.test_manager.remove_test_stats(self.test_id)
        self.test_UI.update_previous_item(question, answer)

    def find_answer_elsewhere(self, given_answer):
        logging.info("{0}:{1}: searching for question: {2}, answer: {3}".format(self.logprefix, "find_answer_elsewhere", self.question, given_answer))
        for i in range(self.itemNumber+1,len(self.test_list)):
            item = self.test_list[i]
            question = ""
            answer = ""
            if self.getDeToEn():
                question =item[1]
                answer = item[2]
            else:
                answer = item[1]
                question =item[2]
            if given_answer == answer and self.question == question:
                try:
                    for previous_answer in self.multi_answer_list[self.question]:
                        if previous_answer == given_answer:
                            logging.info("{0}:{1}: answer already given".format(self.logprefix, "find_answer_elsewhere"))
                            return False
                except:
                    pass
                logging.info("{0}:{1}: found item at: {2}".format(self.logprefix, "find_answer_elsewhere", i))
                logging.info("{0}:{1}: found item: {2}, current: {3}".format(self.logprefix, "find_answer_elsewhere", item, self.test_list[self.itemNumber]))
                self.test_list[i], self.test_list[self.itemNumber] = self.test_list[self.itemNumber], self.test_list[i]
                logging.info("{0}:{1}: after swap: {2}, current: {3}".format(self.logprefix, "find_answer_elsewhere", item, self.test_list[self.itemNumber]))
                if self.getDeToEn():
                    (self.questionId, self.question, self.answer) = self.test_list[self.itemNumber]
                else:
                    (self.questionId, self.answer, self.question) = self.test_list[self.itemNumber]
                logging.info("{0}:{1}: correct answer not already given. Confirm question: {2}, answer: {3}".format(self.logprefix, "find_answer_elsewhere", self.question, self.answer))
                return True
        return False

    def update_results(self, answer):
        logging.info("{0}:{1}: user answer: {2}, correct answer: {3}".format(self.logprefix, "update_results", answer, self.answer))
        logging.info("{0}:{1}: old item list:".format(self.logprefix, "update_results"))
        for elem in self.test_list:
            logging.info("{0}:{1}:            question: {2}, answer: {3}".format(self.logprefix, "update_results", elem[1], elem[2]))
        correct = False
        if answer == self.answer:
            correct = True
        elif self.find_answer_elsewhere(answer):
            correct = True
        else:
            self.wrong_results.append(self.question + " | " + self.answer)
        if correct:
            self.score += 1
            try:
                self.multi_answer_list[self.question].append(self.answer)
                logging.info("{0}:{1}: answer was correct, appended to multi answer list".format(self.logprefix, "update_results"))
            except:
                answer_list = []
                answer_list.append(self.answer)
                self.multi_answer_list[self.question] = answer_list
                logging.info("{0}:{1}: answer was correct, created entry for multi answer list".format(self.logprefix, "update_results"))
        logging.info("{0}:{1}: new item list:".format(self.logprefix, "update_results"))
        for elem in self.test_list:
            logging.info("{0}:{1}:            question: {2}, answer: {3}".format(self.logprefix, "update_results", elem[1], elem[2]))
        done = self.itemNumber + 1
        remaining = len(self.test_list) - done
        wrong = done - self.score
        item = self.question + " | " + self.answer
        logging.info("{0}:{1}: correct: {2}".format(self.logprefix, "update_results", correct))
        if remaining == 0:
            self.test_manager.write_test_resuts(self.user_id, self.test_id, self.dated_score_handler.getNowText(), self.score)
        return (self.score, wrong, done, remaining, correct, item)

    def back_to_edit_test(self):
        self.manager.do_edit_test(self.test_name, self.test_id)
    
    def quit(self):
        self.manager.quit()
