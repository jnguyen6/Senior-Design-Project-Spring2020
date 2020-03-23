"""
Table for records of patient activity
"""

from app import db

class Activity(db.Model):
    activityID = db.Column(db.Integer, primary_key=True)

    accountId = db.Column(db.Integer)
    eventId = db.Column(db.Integer)
    billStatus = db.Column(db.String(20), nullable=False)
    actionDate = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Account Id ={self.accountId} event id={self.eventId} Bill status={self.billStatus} Action Date={self.actionDate}'
