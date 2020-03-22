from app import db

class Communication(db.Model):
    accountId = db.Column(db.Integer, primary_key=True)
    notification_date_time = db.Column(db.String(50), unique=False, nullable=False)
    method = db.Column(db.String(30), unique=False, nullable=False)
    notification_type = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return f'<Communication Account ID={self.accountId} Notification Date Time={self.notification_date_time} Delivery Method={self.method} Notification Type={self.notification_type}'