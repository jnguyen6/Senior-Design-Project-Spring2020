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
    from src.models.Cohort import Cohort
    cohorts = Cohort.query.all()

    ages = [0, 25, 40, 60, 80, -1]
    incomes = [0, 50000, 100000, 150000, 250000, -1]
    bills = [0, 1500, 5000, 10000, 25000, 100000, -1]

    if len(cohorts == 0):
        #Age brackets
        for i in range(1,6):
            ageMax = ages[i]
            ageMin = ages[i-1]
            
            #income brackets
            for i in range(1,6):
                incomeMax = incomes[i]
                incomeMin = incomes[i-1]
                
                #Bill brackets
                for i in range(1,7):
                    billMax = bills[i]
                    billMin = bills[i-1]

                    maleCohort = Cohort()
                    maleCohort.initialize(ageMin, ageMax, 'M', incomeMin, incomeMax, billMin, billMax)
                    db.session.add(maleCohort)

                    femaleCohort = Cohort()
                    femaleCohort.initialize(ageMin, ageMax, 'F', incomeMin, incomeMax, billMin, billMax)
                    db.session.add(femaleCohort)

from src.blueprints.core import bp as bp_core
bp_core.config(app)

from src.blueprints.views import bp as bp_views
bp_views.config(app)
