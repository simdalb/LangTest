
import logging
from common import found_status

class TestManager:
    def __init__(self, cursor, connect):
        self.logprefix = "TestManager"
        self.cursor = cursor
        self.connect = connect

    def get_test_id(self, test_name):
        self.cursor.execute("SELECT testId FROM tests WHERE testName = '" + test_name + "'")
        test_id = -1
        row = self.cursor.fetchone()
        if row != None:
            test_id = row[0]
        logging.info("{0}:{1}: test name: {2} has test id: {3}".format(self.logprefix, "get_test_id", test_name, test_id))
        return test_id
    
    def get_test_name(self, test_id):
        self.cursor.execute("SELECT testName FROM tests WHERE testId = '" + str(test_id) + "'")
        test_name = ""
        row = self.cursor.fetchone()
        if row != None:
            test_name = row[0]
        logging.info("{0}:{1}: test name: {2} has test id: {3}".format(self.logprefix, "get_test_name", test_name, test_name))
        return test_name
    
    def get_tests(self, user_id):
        self.cursor.execute("SELECT testName, testId, timestamp FROM tests")
        rows = self.cursor.fetchall()
        tests = []
        for row in rows:
            self.cursor.execute("SELECT COUNT(*) FROM testContents WHERE testId = '" + str(row[1]) + "'")
            count = self.cursor.fetchone()
            tests.append([row[0], row[1], row[2], count[0]])
        test_list = []
        for test in tests:
            logging.info("{0}:{1}: found test name: {2} in DB".format(self.logprefix, "get_tests", test[0]))
            self.cursor.execute("SELECT score, timestamp FROM stats WHERE userId = '" + str(user_id) + "' AND testId = '" + str(test[1]) + "'")
            rows2 = self.cursor.fetchall()
            test_list.append([test[0], test[1], test[2], test[3], rows2])
        return test_list

    def test_exists(self, test_name):
        return self.get_test_id(test_name) != -1
    
    def getTestList(self, test_id):
        self.cursor.execute("SELECT questionId, termLang1, termLang2 FROM testContents WHERE testId = '" + str(test_id) + "'")
        return self.cursor.fetchall()

    def get_matches(self, text):
        logging.info("{0}:{1}: searching for test names that match text: {2}".format(self.logprefix, "get_matches", text))
        self.cursor.execute("SELECT testName FROM tests WHERE testName LIKE '" + text + "'")
        test_name_list = []
        for (test_name,) in self.cursor.fetchall():
            logging.info("{0}:{1}: test name: {2} matches text".format(self.logprefix, "get_matches", test_name))
            test_name_list.append(test_name)
        return test_name_list

    def create_test(self, test_name, timestamp):
        logging.info("{0}:{1}: creating test name: {2}".format(self.logprefix, "create_test", test_name))
        self.cursor.execute("INSERT INTO tests (testName, timestamp) VALUES ('" + test_name + "', '" + timestamp + "')")
        self.connect.commit()
        return self.get_test_id(test_name)
    
    def get_number_of_tests(self):
        self.cursor.execute("SELECT COUNT(*) FROM tests")
        row = self.cursor.fetchone()
        count = row[0]
        logging.info("{0}:{1}: number of tests: {2}".format(self.logprefix, "getNumberOfItems", count))
        return count
    
    def get_other_tests(self, test_id):
        self.cursor.execute("SELECT testId, testName FROM tests WHERE NOT testId = '" +  str(test_id) + "'")
        rows = self.cursor.fetchall()
        test_list = []
        for row in rows:
            test_list.append([row[0], row[1], self.getNumberOfItems(row[0])])
        return test_list
    
    def getNumberOfItems(self, test_id):
        self.cursor.execute("SELECT COUNT(*) FROM testContents WHERE testId = '" + str(test_id) + "'")
        row = self.cursor.fetchone()
        logging.info("{0}:{1}: test id: {2} has {3} items".format(self.logprefix, "getNumberOfItems", test_id, row[0]))
        return row[0]
    
    def get_similar_results(self, test_id, german_value, english_value):
        ret_list = []
        self.cursor.execute("SELECT termLang1 FROM testContents WHERE termLang2 = '" +  english_value 
                            + "' AND testId = '" + str(test_id) + "' AND NOT termLang1 = '" + german_value + "'")
        rows = self.cursor.fetchall()
        if rows:
            terms = []
            for row in rows:
                terms.append(row[0])
            ret_list.append([found_status.FoundStatus.DE_FOUND, terms])
        self.cursor.execute("SELECT termLang2 FROM testContents WHERE termLang1 = '" +  german_value 
                            + "' AND testId = '" + str(test_id) + "' AND NOT termLang2 = '" + english_value + "'")
        rows = self.cursor.fetchall()
        if rows:
            terms = []
            for row in rows:
                terms.append(row[0])
            ret_list.append([found_status.FoundStatus.EN_FOUND, terms])
        return ret_list
    
    def check_status(self, test_id, german_value, english_value):
        ret_list = []
        found_test_name_to_values = dict()
        self.cursor.execute("SELECT testId FROM testContents WHERE termLang1 = '" +  german_value 
                            + "' AND termLang2 = '" + english_value + "'")
        rows = self.cursor.fetchone()
        if rows:
            found_test_name_to_values.setdefault(self.get_test_name(rows[0]), [])
            ret_list.append((found_status.FoundStatus.BOTH_FOUND, found_test_name_to_values, german_value, english_value))
            return ret_list
        self.cursor.execute("SELECT testId, termLang2 FROM testContents WHERE termLang1 = '" + german_value + "'")
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                if not row[0] == test_id:
                    found_test_name_to_values.setdefault(self.get_test_name(row[0]), []).append(row[1])
            if(found_test_name_to_values):
                ret_list.append((found_status.FoundStatus.DE_FOUND, found_test_name_to_values, german_value, english_value))
        self.cursor.execute("SELECT testId, termLang1 FROM testContents WHERE termLang2 = '" + english_value + "'")
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                if not row[0] == test_id:
                    found_test_name_to_values.setdefault(self.get_test_name(row[0]), []).append(row[1])
            if(found_test_name_to_values):
                ret_list.append((found_status.FoundStatus.EN_FOUND, found_test_name_to_values, german_value, english_value))
        return ret_list

    def append_item(self, test_id, german_value, english_value):
        logging.info("{0}:{1}: appending German: {2}, English: {3}".format(self.logprefix, "append_item", german_value, english_value))
        ret_list = self.check_status(test_id, german_value, english_value)
        if not ret_list:
            found_test_name_to_values = dict()
            self.cursor.execute("INSERT INTO testContents (testId, termLang1, termLang2) VALUES ('" 
                                + str(test_id) + "','" + german_value + "','" + english_value + "')")
            self.connect.commit()
            ret_list.append((found_status.FoundStatus.NONE_FOUND, found_test_name_to_values, german_value, english_value))
        return ret_list
    
    def get_question_id(self, german_value, english_value):
        self.cursor.execute("SELECT questionId FROM testContents WHERE termLang1 = '" + german_value 
                            + "' AND termLang2 = '" + english_value + "'")
        row = self.cursor.fetchone()
        return row[0]
    
    def delete_item(self, questionId):
        self.cursor.execute("DELETE FROM testContents WHERE questionId = '" + str(questionId) + "'")
        self.connect.commit()
        
    def move_item(self, questionId, test_id):
        self.cursor.execute("UPDATE testContents SET testId = '" + str(test_id) + "' WHERE questionId = '" + str(questionId) + "'")
        self.connect.commit()

    def append_item_to_other_test(self, test_name, german_value, english_value):
        logging.info("{0}:{1}: appending german_value: {2}, english_value: {3} to test: {4}".format(self.logprefix, 
                                                                                                    "append_item_to_other_test", 
                                                                                                    german_value,
                                                                                                    english_value,
                                                                                                    test_name))
        self.cursor.execute("INSERT INTO testContents (testId, termLang1, termLang2) VALUES ('" 
                            + str(self.get_test_id(test_name)) + "','" + german_value + "','" + english_value + "')")
        self.connect.commit()
        
    def modify_question(self, test_id, questionId, german_value, english_value):
        logging.info("{0}:{1}: changing to german_value: {2}, english_value: {3} for question id: {4}".format(self.logprefix, 
                                                                                                              "modify_question", 
                                                                                                              german_value,
                                                                                                              english_value,
                                                                                                              questionId))
        ret_list = self.check_status(test_id, german_value, english_value)
        if not ret_list:
            found_test_name_to_values = dict()
            self.cursor.execute("UPDATE testContents SET termLang1 = '" + german_value + "', termLang2 = '" + english_value \
                                + "' WHERE questionId = '" + str(questionId) + "'")
            self.connect.commit()
            ret_list.append((found_status.FoundStatus.NONE_FOUND, found_test_name_to_values, german_value, english_value))
        return ret_list

    def getMatches(self, expr, testId):
        logging.info("{0}:{1}: searching for expression: {2} in testId: {3}".format(self.logprefix, "getMatches", expr, testId))
        self.cursor.execute("SELECT questionId, termLang1, termLang2 FROM testContents WHERE (termLang1 LIKE '%" + expr 
                            + "%' OR termLang2 LIKE '%" + expr + "%') AND testId = '" + str(testId) + "'")
        return self.cursor.fetchall()
        
    def delete_test(self, test_id):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rows = self.cursor.fetchall()
        for row in rows:
            logging.info("{0}:{1}: found database {2}".format(self.logprefix, "delete_test", row[0]))
            try:
                self.cursor.execute("DELETE FROM " + row[0] + " WHERE testId = '" + str(test_id) + "'")
                self.connect.commit()
            except:
                pass

    def getAllItems(self, test_id):
        self.cursor.execute("SELECT termLang1, termLang2 FROM testContents WHERE testId = '" + str(test_id) + "'")
        return self.cursor.fetchall()