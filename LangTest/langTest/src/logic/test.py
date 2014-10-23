
import logging

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
        self.itemNumber = -1
        self.questionId = -1
        self.question = ""
        self.answer = ""
        self.score = 0
        
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
        self.itemNumber += 1
        if self.getDeToEn():
            (self.questionId, self.question, self.answer) = self.test_list[self.itemNumber]
        else:
            (self.questionId, self.answer, self.question) = self.test_list[self.itemNumber]
        return self.question
    
    def getAnswer(self):
        return self.answer
    
    def update_results(self, answer):
        logging.info("{0}:{1}: user answer: {2}, correct answer: {3}".format(self.logprefix, "update_results", answer, self.answer))
        correct = False
        if answer == self.answer:
            logging.info("{0}:{1}: answer was correct".format(self.logprefix, "update_results"))
            correct = True
            self.score += 1
        done = self.itemNumber + 1
        remaining = len(self.test_list) - done
        wrong = done - self.score
        item = self.question + " | " + self.answer
        logging.info("{0}:{1}: correct: {2}".format(self.logprefix, "update_results", correct))
        return (self.score, wrong, done, remaining, correct, item)
    
    def back_to_edit_test(self):
        self.manager.do_edit_test(self.test_name, self.test_id)
    
    def quit(self):
        self.manager.quit()

    