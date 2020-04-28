import json

import requests
from flask import render_template, request
from pytz import timezone

from app import db
from src.algorithms.categorize import categorizeFromBuckets
from src.blueprints.core.routes import get_cohorts
from src.blueprints.views.bp import bp
from src.models.Cohort import Cohort
from src.models.Communication import Communication
from src.models.QueueJob import QueueJob
from src.models.QueueStatus import QueueStatus


# show the landing page view when accessing the app
@bp.route("/")
def index():
    return render_template('index.html')

# @bp.route("/view/users")
# def get_users_default():

#     return get_users(0)

# @bp.route("/view/users")
# def get_users():

#     comms = Communication.query.all()
#     userList = []
#     count = 0
#     currentIdx = 0
#     # smallList = []
#     for com in comms:
#         count = count + 1
#         comDict = dict()
#         comDict['ID'] = com.accountId
#         comDict['date/time'] = com.notification_date_time
#         comDict['method'] = com.method
#         comDict['type'] = com.notification_type
#         userList.append(comDict)

#         if count == 20:
#             # userList.append(smallList)
#             # smallList = []
#             # if currentIdx == idx:
#             # for right now, only send the first 20 entries
#             break

#     return render_template('users.html', users=userList)

@bp.route('/view/user', methods=['POST', 'GET'])
def get_cohort_by_user_stats():
  if request.method == 'POST':
      form = request.form
      # print(form)
      patientDict = dict()
      patientDict['id'] = 0
      # print(form['fullDateOfBirth'])

      patientDict['dateOfBirth'] = int(form['fullDateOfBirth'][:4])
      if form['gender'] == "male":
        patientDict['gender'] = 'M'
      else:
        patientDict['gender'] = 'F'
      patientDict['income'] = int(form['income'])
      patientDict['billAmount'] = int(form['billAmount'])
      patientDict['OptOut'] = form['optOut']

      print(patientDict)
      cID = str(categorizeFromBuckets(patientDict))
      patientDict['paperID'] = cID[0]
      patientDict['textID'] = cID[1]
      patientDict['emailID'] = cID[2]
      patientDict['fullDateOfBirth'] = form['fullDateOfBirth']

      return render_template("user-form-single.html", cohort=patientDict)
  return render_template("user-form.html", cohort="")

@bp.route("/view/cohorts")
def get_cohorts_view():
    c = Cohort.query.all()
    # print(c)
    cohortSet = set()
    for cohort in c:
        cohortSet.add(cohort.cid)
    cohortList = []
    for cohortID in cohortSet:
        cDict = dict()
        cDict['cohort ID'] = cohortID
        cID = str(cohortID)
        cDict['papers per cycle'] = cID[0]
        cDict['texts per cycle'] = cID[1]
        cDict['emails per cycle'] = cID[2]
        cohortList.append(cDict)
    # print(result)
    # cohortList = {'cohort ID' : cohortSet}
    cohortList = sorted(cohortList, key=lambda k:k['cohort ID'])
    # print(cohortList)
    return render_template('cohorts.html', cohorts=cohortList)

@bp.route("/view/cohorts/<int:cohortID>")
def get_patients_by_cohort(cohortID):
    c = Cohort.query.filter_by(cid=cohortID).all()
    cohortList = []
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

# Retrieve a list of jobs currently in the job queue database
@bp.route("/view/jobs")
def get_jobs():
    jobs = QueueJob.query.all()
    jobListUnsorted = []
    for job in jobs:
        jobDict = dict()
        jobDict['job ID'] = job.id
        jobDict['status'] = get_status(job.status)
        jobDict['job algorithm'] = job.algorithm
        jobDict['date created'] = get_pretty_date(job.date_created)
        jobListUnsorted.append(jobDict)

    jobList = sorted(jobListUnsorted, key=lambda k:k['job ID'])

    return render_template('jobs.html', jobs=jobList)

def get_status(key):
    return QueueStatus(key).name.replace('_', ' ')

def get_pretty_date(oldDate):
    newDate = timezone('US/Eastern').fromutc(oldDate)
    return newDate.strftime("%d %b %Y at %H:%M")
