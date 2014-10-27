
from datetime import datetime
from datetime import timedelta
import logging

class DatedScoreHandler:
    def __init__(self):
        self.logprefix = "DatedScoreHandler"
        logging.info("{0}:{1}:".format(self.logprefix, "__init__"))
        self.format = "%b %d %Y %H:%M:%S"
        
    def effective_score(self, total, score_timestamp_list, creation_time_text):
        creation_time = datetime.strptime(creation_time_text, self.format)
        most_recent_timestamp = creation_time
        one_week = datetime.strptime("Jan 01 2014 12:00:00", self.format) - datetime.strptime("Jan 08 2014 12:00:00", self.format)
        time_since_last_test = one_week
        score = 0
        score_frac = float(score) / float(total)
        timestamp_now = datetime.utcnow()
        pre_effective_score = 0
        if score_timestamp_list:
            most_recent_score_timestamp = score_timestamp_list[0]
            most_recent_timestamp = datetime.strptime(most_recent_score_timestamp[1], self.format)
            logging.info("{0}:{1}: most recent timestamp: {2}".format(self.logprefix, "effective_score", most_recent_timestamp))
            for score_timestamp in score_timestamp_list:
                timestamp = datetime.strptime(score_timestamp[1], self.format)
                logging.info("{0}:{1}: timestamp: {2}".format(self.logprefix, "effective_score", timestamp))
                if  timestamp > most_recent_timestamp:
                    most_recent_score_timestamp = score_timestamp
                    most_recent_timestamp = timestamp
            score = most_recent_score_timestamp[0] / float(total)
            timestamp = most_recent_score_timestamp[1]
            time_since_last_test = datetime.utcnow() - datetime.strptime(timestamp, self.format)
            pre_effective_score = max(0, score_frac - 0.05 * float(time_since_last_test.total_seconds()) / float(one_week.total_seconds()))
        time_since_created = timestamp_now - creation_time
        time_of_zero_pre_effective_score = most_recent_timestamp + timedelta(seconds=int(score_frac * 20 * one_week.total_seconds()))
        time_since_zero_pre_effective_score = timestamp_now - time_of_zero_pre_effective_score
        return pre_effective_score - (0 if score_timestamp_list else time_since_created.seconds) \
                                   - (time_since_zero_pre_effective_score.seconds if score_timestamp_list and pre_effective_score == 0 else 0)
    
    def getNowText(self):
        datetime.strftime(datetime.utcnow(), self.format)
