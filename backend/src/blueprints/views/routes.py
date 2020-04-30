import json

import requests
from flask import render_template, request
from pytz import timezone

from app import db
from src.algorithms.categorize import categorizeFromBuckets
from src.blueprints.core.routes import get_cohorts, create_job
from src.blueprints.views.bp import bp
from src.models.Cohort import Cohort
from src.models.Communication import Communication
from src.models.QueueJob import QueueJob
from src.models.QueueStatus import QueueStatus


# show the landing page view when accessing the app
@bp.route("/")
def index():
    return render_template('index.html')

# returns a form that allows patient demographics input
# if a POST request, the inputted patient data and the corresponding cohort data are returned
@bp.route('/view/user', methods=['POST', 'GET'])
def get_cohort_by_user_stats():
    if request.method == 'POST':

        # grab patient stats from form
        form = request.form
        patientDict = dict()
        patientDict['id'] = 0
        patientDict['dateOfBirth'] = int(form['fullDateOfBirth'][:4])
        if form['gender'] == "male":
            patientDict['gender'] = 'M'
        else:
            patientDict['gender'] = 'F'
        patientDict['income'] = int(form['income'])
        patientDict['billAmount'] = int(form['billAmount'])
        patientDict['OptOut'] = form['optOut']

        # find where this patient falls into a cohort
        cID = str(categorizeFromBuckets(patientDict))
        patientDict['paperID'] = cID[0]
        patientDict['textID'] = cID[1]
        patientDict['emailID'] = cID[2]
        patientDict['fullDateOfBirth'] = form['fullDateOfBirth']

        return render_template("user-form-single.html", cohort=patientDict)

    return render_template("user-form.html")

# returns a human-reable table of the current cohorts in the database (grouped by cohort ID)
@bp.route("/view/cohorts")
def get_cohorts_view():

    # gather all cohort IDs (non-duplicates)
    cohorts = Cohort.query.all()
    cohortSet = set()
    for cohort in cohorts:
        cohortSet.add(cohort.cid)

    # add each cohort ID to the list
    cohortList = []
    for cohortID in cohortSet:
        cDict = dict()
        cDict['cohort ID'] = cohortID
        cID = str(cohortID)
        cDict['papers per cycle'] = cID[0]
        cDict['texts per cycle'] = cID[1]
        cDict['emails per cycle'] = cID[2]
        cohortList.append(cDict)

    cohortList = sortList(cohortList, 'cohort ID')

    return render_template('cohorts.html', cohorts=cohortList)

# returns the cohorts of a given cohort ID
@bp.route("/view/cohorts/<int:cohortID>")
def get_by_cohort_id(cohortID):
    cohortList = []

    c = Cohort.query.filter_by(cid=cohortID).all()
    for cohort in c:
        cDict = dict()
        # cDict['cohort ID'] = cohort.cid
        cDict['minimum age'] = cohort.ageMin
        cDict['maximum age'] = cohort.ageMax
        cDict['gender'] = cohort.gender
        cDict['minimum income'] = cohort.incomeMin
        cDict['maximum income'] = cohort.incomeMax
        cDict['minimum bill amount'] = cohort.billAmountMin
        cDict['maximum bill amount'] = cohort.billAmountMax
        cohortList.append(cDict)

    return render_template('cohorts-single.html', cohortID=cohortID, cohorts=cohortList)

# returns a user-readble table of the current jobs in the database
# if a POST request is made, the job is created with the specified algorithm
@bp.route("/view/jobs", methods=['POST', 'GET'])
def get_jobs():
    if request.method == 'POST':
        create_job(request.form['algorithm'])

    jobListUnsorted = []

    jobs = QueueJob.query.all()
    for job in jobs:
        jobDict = dict()
        jobDict['job ID'] = job.id
        jobDict['status'] = get_status(job.status)
        jobDict['job algorithm'] = job.algorithm.replace('_', ' ')
        jobDict['date created'] = get_pretty_date(job.date_created)
        jobListUnsorted.append(jobDict)

    jobList = sortList(jobListUnsorted, 'job ID')

    return render_template('jobs.html', jobs=jobList)

# returns a user-readable queue status
def get_status(key):
    return QueueStatus(key).name.replace('_', ' ')

# returns a pretty date converted from UTC to US/Eastern
def get_pretty_date(oldDate):
    newDate = timezone('US/Eastern').fromutc(oldDate)
    return newDate.strftime("%d %b %Y at %H:%M")

# returns a list of dictionaries (unsortedList) sorted by a key (key)
def sortList(unsortedList, key):
    return sorted(unsortedList, key=lambda k:k[key])
