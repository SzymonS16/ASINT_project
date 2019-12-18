import secretariat
import pickle


class secretariatDB:
    def __init__(self, name):
        self.name = name
        try:
            f = open('scr_dump' + name, 'rb')
            self.scr = pickle.load(f)
            f.close()
        except IOError:
            self.scr = {}

    def addSecretariat(self, location, name, description, opening_hours):
        scr_id = len(self.scr)
        self.scr[scr_id] = secretariat.Secretariat(scr_id, location, name, description, opening_hours)
        f = open('scr_dump' + self.name, 'wb')
        pickle.dump(self.scr, f)
        f.close()
        return self.scr[scr_id]

    def showSecretariat(self, scr_id):
        if scr_id >= len(self.scr):
            return None
        else:
            return self.scr[scr_id]

    def listAllSecretariats(self):
        return list(self.scr.values())

    def editSecretariat(self, scr_id, location, name, description, opening_hours):
        self.scr[scr_id] = secretariat.Secretariat(scr_id, location, name, description, opening_hours)
        f = open('scr_dump' + self.name, 'wb')
        pickle.dump(self.scr, f)
        f.close()
        return self.scr[scr_id]
