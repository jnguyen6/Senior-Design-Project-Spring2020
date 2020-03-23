from app import db


"""
Table for record of communications with the patient
"""
class Communications(db.model):
    eventId = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.Integer)
    notificationDate = db.Column(db.String(30), nullable=False)
    deliveryMethod = db.Column(db.String(30), nullable=False)
    notifType = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Account Id ={self.accountId} Date of notification={self.notificationDate} Delivery Method={self.deliveryMethod} Notification Type={self.notifType}'
