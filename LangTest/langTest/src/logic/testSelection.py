
import logging
from datetime import datetime

class TestSelection:
    def __init__(self, manager, UI_factory, test_manager, user_name, user_id):
        self.logprefix = "TestSelection"
        logging.info("{0}:{1}:".format(self.logprefix, "__init__"))
        self.manager = manager
        self.UI_factory = UI_factory
        self.test_selection_UI = UI_factory.create_test_selection_UI()
        self.test_manager = test_manager
        self.user_name = user_name
        self.user_id = user_id
        
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
        test_list.sort(key=lambda(test):self.effective_score(test))
        return test_list

    def recommendedTest(self, test1, test2):
        eff_score1 = self.effective_score(test1)
        eff_score2 = self.effective_score(test2)
        if eff_score1 < eff_score2:
            return 1
        elif eff_score1 == eff_score2:
            return 0
        else:
            return -1

    def effective_score(self, test):
        total = test[3]
        score_timestamp_list = test[4]
        creation_time = datetime.strptime(test[2], "%b %d %Y %H:%M:%S")
        score = 0
        timestamp_now = datetime.utcnow()
        pre_effective_score = 0
        if score_timestamp_list:
            most_recent_score_timestamp = score_timestamp_list[0]
            most_recent_timestamp = datetime.strptime(most_recent_score_timestamp[1], "%b %d %Y %H:%M:%S")
            for score_timestamp in score_timestamp_list:
                timestamp = datetime.strptime(score_timestamp[1], "%b %d %Y %H:%M:%S")
                if  timestamp - most_recent_timestamp > 0:
                    most_recent_score_timestamp = score_timestamp
                    most_recent_timestamp = timestamp
            score = most_recent_score_timestamp[0] / float(total)
            timestamp = most_recent_score_timestamp[1]
            time_since_last_test = self.current_time - datetime.strptime(timestamp, "%b %d %Y %H:%M:%S")
            pre_effective_score = max(0, score - 0.1 * time_since_last_test.weeks)
        time_since_created = timestamp_now - creation_time
        time_of_zero_pre_effective_score = time_since_last_test + score * 10 * (datetime.strptime("Jan 01 2014 12:00:00", "%b %d %Y %H:%M:%S")
                                                                              - datetime.strptime("Jan 08 2014 12:00:00", "%b %d %Y %H:%M:%S"))
        time_since_zero_pre_effective_score = timestamp_now - time_of_zero_pre_effective_score
        return pre_effective_score - (0 if score_timestamp_list else time_since_created.seconds) \
                                   - (time_since_zero_pre_effective_score.seconds if score_timestamp_list and pre_effective_score == 0 else 0)
    
    def inform_test_exists(self, test_name):
        self.UI_factory.create_InformTestExistsPopupWindow(self.test_selection_UI).start(test_name)
    
    def test_exists(self, test_name):
        return self.test_manager.test_exists(test_name)
        
    def receive_partial_text(self, text):
        return self.test_manager.get_matches(text)
    
    def create_test(self, test_name):
        logging.info("{0}:{1}: creating test: {2}".format(self.logprefix, "create_test", test_name))
        self.test_selection_UI.finish()
        test_id = self.test_manager.create_test(test_name, datetime.strftime(datetime.utcnow(), "%b %d %Y %H:%M:%S"))
        self.manager.do_edit_test(test_name, test_id)

    def prompt_new_test(self, test_name):
        logging.info("{0}:{1}: creating test: {2}".format(self.logprefix, "prompt_new_test", test_name))
        self.UI_factory.create_CreateTestPopupWindow(self.test_selection_UI).start(test_name, self)
        
    def quit(self):
        self.manager.quit()
    
    def back_to_login(self):
        self.manager.do_login()