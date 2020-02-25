import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://admin:Password1!@db:5432/backend')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from src.models import QueueJob, Cohort

@app.before_first_request
def create_tables():
    db.create_all()

from src.blueprints.core import bp as bp_core
bp_core.config(app)
