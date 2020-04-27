from enum import Enum
from app import db
from datetime import datetime

class QueueJob(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    # For now, I set the default value to 0 instead of QueueStatus.NOT_STARTED. For some reason, the error
    # sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) can't adapt type 'QueueStatus'
    # is thrown.
    status = db.Column(db.Integer, nullable = False, default = 0)
    algorithm = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'<QueueJob id={self.id} status={self.status}'
