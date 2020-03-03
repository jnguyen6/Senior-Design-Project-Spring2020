from enum import Enum
from app import db

class QueueStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    DONE = 2
    CANCELED = 3
