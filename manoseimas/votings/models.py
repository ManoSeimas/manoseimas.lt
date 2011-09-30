from manoseimas.couchdb import Document


class Voting(Document):
    def did_not_vote(self):
        joined = int(self.registration['joined'])
        total = int(self.total_votes)
        return joined - total
