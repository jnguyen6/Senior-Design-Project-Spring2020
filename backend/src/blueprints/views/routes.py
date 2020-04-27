from src.blueprints.views.bp import bp
from flask import request
from flask import render_template
from app import db
from pytz import timezone
from src.models import QueueJob
from src.models.QueueStatus import QueueStatus
from src.models.Communication import Communication
from src.models.Cohort import Cohort

# show the landing page view when accessing the app
@bp.route("/")
def index():

    return render_template('index.html')

# @bp.route("/view/users")
# def get_users_default():

#     return get_users(0)

@bp.route("/view/users")
def get_users():

    comms = Communication.query.all()
    userList = []
    count = 0
    currentIdx = 0
    # smallList = []
    for com in comms:
        count = count + 1
        comDict = dict()
        comDict['ID'] = com.accountId
        comDict['date/time'] = com.notification_date_time
        comDict['method'] = com.method
        comDict['type'] = com.notification_type
        userList.append(comDict)

        if count == 20:
            # userList.append(smallList)
            # smallList = []
            # if currentIdx == idx:
            # for right now, only send the first 20 entries
            break

    return render_template('users.html', users=userList)

@bp.route("/view/cohorts")
def get_cohorts():

    c = Cohort.query.all()
    cohortList = []
    for cohort in c:
        cDict = dict()
        cDict['cohort ID'] = cohort.cid
        cDict['papers per cycle'] = cohort.paper
        cDict['texts per cycle'] = cohort.text
        cDict['emails per cycle'] = cohort.email
        cDict['minimum age'] = cohort.ageMin
        cDict['maximum age'] = cohort.ageMax
        cDict['gender'] = cohort.gender
        cDict['minimum income'] = cohort.incomeMin
        cDict['maximum income'] = cohort.incomeMax
        cDict['minimum bill amount'] = cohort.billAmountMin
        cDict['maximum bill amount'] = cohort.billAmountMax
        cohortList.append(cDict)

    return render_template('cohorts.html', cohorts=cohortList)

@bp.route("/view/cohorts/<int:idx>")
def get_patients_by_cohort(id):

    c = Cohort.query.all()
    cohortList = []
    # for cohort in c:
    #     cDict = dict()
    #     cDict['cohort ID'] = cohort.cid
    #     cDict['paper'] = cohort.paper
    #     cDict['text'] = cohort.text
    #     cDict['email'] = cohort.email
    #     cohortList.append(cDict)

    return render_template('cohorts.html', cohorts=cohortList)

# Retrieve a list of jobs currently in the job queue database
@bp.route("/view/jobs")
def get_jobs():

    jobs = QueueJob.QueueJob.query.all()
    jobListUnsorted = []
    for job in jobs:
        jobDict = dict()
        jobDict['job ID'] = job.id
        jobDict['status'] = get_status(job.status)
        jobDict['job algorithm'] = job.algorithm
        jobDict['date created'] = get_pretty_date(job.date_created)
        jobListUnsorted.append(jobDict)
    # jobList.sort()
    jobList = sorted(jobListUnsorted, key=lambda k:k['job ID'])
    # {k: v for k,v in sorted(jobList.items(), key=lambda item:item[1])}
    return render_template('jobs.html', jobs=jobList)

def get_status(key):

    return QueueStatus(key).name.replace('_', ' ')

def get_pretty_date(oldDate):

    newDate = timezone('US/Eastern').fromutc(oldDate)
    return newDate.strftime("%d %b %Y at %H:%M")
