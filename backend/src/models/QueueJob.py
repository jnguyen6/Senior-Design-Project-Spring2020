from enum import Enum
from app import db
from datetime import datetime

class QueueStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    DONE = 2
    CANCELLED = 3

class QueueJob(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.Integer, nullable = False, default = QueueStatus.NOT_STARTED)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'<QueueJob id={self.id} status={self.status}'
