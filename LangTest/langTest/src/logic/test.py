
import logging
import random
from datetime import datetime

class Test:
    def __init__(self, manager, UI_factory, test_manager, persistency_manager, user_name, user_id, test_name, test_id):
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
        self.test_list = []
        self.wrong_results = []
        self.itemNumber = -1
        self.questionId = -1
        self.question = ""
        self.answer = ""
        self.score = 0
        self.multi_answer_list = dict()
        
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
        
    def find_answer_elsewhere(self, given_answer):
        for item in self.test_list:
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
                            return False
                except:
                    pass
                item, self.test_list[self.itemNumber] = self.test_list[self.itemNumber], item
                return True
        return False
    
    def update_results(self, answer):
        logging.info("{0}:{1}: user answer: {2}, correct answer: {3}".format(self.logprefix, "update_results", answer, self.answer))
        correct = False
        if answer == self.answer:
            correct = True
        elif self.find_answer_elsewhere(answer):
            correct = True
        else:
            self.wrong_results.append(self.question + " | " + self.answer)
        if correct:
            logging.info("{0}:{1}: answer was correct".format(self.logprefix, "update_results"))
            self.score += 1
            try:
                self.multi_answer_list[self.question].append(self.answer)
            except:
                answer_list = []
                answer_list.append(self.answer)
                self.multi_answer_list[self.question] = answer_list
        done = self.itemNumber + 1
        remaining = len(self.test_list) - done
        wrong = done - self.score
        item = self.question + " | " + self.answer
        logging.info("{0}:{1}: correct: {2}".format(self.logprefix, "update_results", correct))
        if remaining == 0:
            self.test_manager.write_test_resuts(self.user_id, self.test_id, datetime.strftime(datetime.utcnow(), "%b %d %Y %H:%M:%S"), self.score)
        return (self.score, wrong, done, remaining, correct, item)
    
    def back_to_edit_test(self):
        self.manager.do_edit_test(self.test_name, self.test_id)
    
    def quit(self):
        self.manager.quit()
