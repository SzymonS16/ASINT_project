import log
import pickle
from datetime import datetime

class logDB:
    def __init__(self, name):
        self.name = name
        try:
            f = open('log_dump' + name, 'rb')
            self.log = pickle.load(f)
            f.close()
        except IOError:
            self.log = {}

    def addLog(self, service, method, resource, status):
        log_id = len(self.log)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log[log_id] = log.log(log_id, timestamp, service, method, resource, status)
        f = open('log_dump' + self.name, 'wb')
        pickle.dump(self.log, f)
        f.close()
        return self.log[log_id]

    def showLog(self, log_id):
        return self.log[log_id]

    def listAllLogs(self):
        return list(self.log.values())
