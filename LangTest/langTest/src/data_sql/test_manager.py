
import logging

class TestManager:
    def __init__(self, cursor, connect):
        self.logprefix = "TestManager"
        self.cursor = cursor
        self.connect = connect
    
    def get_test_id(self, test_name):
        self.cursor.execute("SELECT testId FROM tests WHERE testName = '" + test_name + "'")
        testId = -1
        row = self.cursor.fetchone()
        if row != None:
            testId = row[0]
        logging.info("{0}:{1}: test name: {2} has test id: {3}".format(self.logprefix, "get_test_id", test_name, testId))
        return testId
    
    def get_tests(self):
        self.cursor.execute("SELECT testName FROM tests")
        test_name_list = []
        for (test_name,) in self.cursor.fetchall():
            logging.info("{0}:{1}: found test name: {2} in DB".format(self.logprefix, "get_tests", test_name))
            test_name_list.append(test_name)
        return test_name_list
    
    def test_exists(self, test_name):
        return self.get_test_id(test_name) != -1

    def get_matches(self, text):
        logging.info("{0}:{1}: searching for test names that match text: {2}".format(self.logprefix, "get_matches", text))
        self.cursor.execute("SELECT testName FROM tests WHERE testName LIKE '" + text + "'")
        test_name_list = []
        for (test_name,) in self.cursor.fetchall():
            logging.info("{0}:{1}: test name: {2} matches text".format(self.logprefix, "get_matches", test_name))
            test_name_list.append(test_name)
        return test_name_list

    def create_test(self, test_name):
        logging.info("{0}:{1}: creating test name: {2}".format(self.logprefix, "create_test", test_name))
        self.cursor.execute("INSERT INTO tests (testName) VALUES ('" + test_name + "')")
        self.connect.commit()
        return self.get_test_id(test_name)
    