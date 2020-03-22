import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://admin:Password1!@localhost/backend')

db = SQLAlchemy(app)

from src.models import QueueJob, Cohort

@app.before_first_request
def create_tables():
    db.create_all()

"""
Populate buckets of cohorts
#TODO need clarification on if tables need to be created on startup always
Seems like they would not
"""
#@app.before_first_request
def populateCohorts():
    None

from src.blueprints.core import bp as bp_core
bp_core.config(app)

from src.blueprints.views import bp as bp_views
bp_views.config(app)
