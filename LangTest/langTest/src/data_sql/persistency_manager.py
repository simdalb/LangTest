
import logging

class PersistencyManager:
    def __init__(self, cursor, connect):
        self.logprefix = "PersistencyManager"
        self.cursor = cursor
        self.connect = connect
    
    def getDeToEn(self, user_id):
        self.cursor.execute("SELECT DeToEn FROM userPersistency WHERE userId = '" + str(user_id) + "'")
        DeToEn = 1
        row = self.cursor.fetchone()
        if row != None:
            DeToEn = row[0]
        logging.info("{0}:{1}: user_id: {2} has DeToEn: {3}".format(self.logprefix, "getDeToEn", user_id, DeToEn))
        return True if DeToEn == 1 else False
    
    def setDeToEn(self, DeToEn, user_id):
        logging.info("{0}:{1}: setting DeToEn: {2} for user_id: {3}".format(self.logprefix, "setDeToEn", str(1 if DeToEn else 0), user_id))
        self.cursor.execute("UPDATE userPersistency SET DeToEn = '" + str(1 if DeToEn else 0) + "' WHERE userId = '" + str(user_id) + "'")
        self.connect.commit()
        newDeToEn = self.getDeToEn(user_id)
        logging.info("{0}:{1}: Now DeToEn: {2} for user_id: {3}".format(self.logprefix, "setDeToEn", newDeToEn, user_id))
        