
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
    
    def getNumberOfItems(self, test_id):
        self.cursor.execute("SELECT COUNT(*) FROM testContents WHERE testId = '" + str(test_id) + "'")
        row = self.cursor.fetchone()
        count = -1
        if row != None:
            count = row[0]
        logging.info("{0}:{1}: test id: {2} has {3} items".format(self.logprefix, "getNumberOfItems", test_id, count))
        return count

    def append_item(self, test_id, german_value, english_value):
        logging.info("{0}:{1}: appending German: {2}, English: {3}".format(self.logprefix, "append_item", german_value, english_value))
        found_test_name_to_values = dict()
        ret_list = []
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
        if ret_list:
            return ret_list
        self.cursor.execute("INSERT INTO testContents (testId, termLang1, termLang2) VALUES ('" 
                            + str(test_id) + "','" + german_value + "','" + english_value + "')")
        self.connect.commit()
        ret_list.append((found_status.FoundStatus.NONE_FOUND, found_test_name_to_values, german_value, english_value))
        return ret_list

    def append_item_to_other_test(self, test_name, german_value, english_value):
        self.cursor.execute("INSERT INTO testContents (testId, termLang1, termLang2) VALUES ('" 
                            + str(self.get_test_id(test_name)) + "','" + german_value + "','" + english_value + "')")
        self.connect.commit()