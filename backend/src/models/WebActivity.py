from app import db

class WebActivity(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.Integer, unique=False, nullable=False)
    eventId = db.Column(db.Integer, unique=False, nullable=False)
    billStatus = db.Column(db.String(30), unique=False, nullable=False)
    actionDate = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return f'<Assigned Unique ID={self.uid} Account ID={self.accountId} Event ID={self.eventId} Bill Status={self.billStatus} Action Date={self.actionDate}'