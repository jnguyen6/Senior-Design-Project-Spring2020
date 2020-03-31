from src.blueprints.core.bp import bp
from flask import request
from flask import jsonify, Response
from app import db
from src.models.Cohort import Cohort
from src.models.Communication import Communication
import json

# Converts the object into a JSON format to be sent as part a response message
def build_json_response(obj):
    return Response(obj, content_type='application/json')

# Returns the usage information for filtering the job queue
def usage_info_filter():
    usage_info = "Invalid argument. To filter the list of jobs in the job queue,"
    usage_info += " provide the following information in the GET request url:\n"
    usage_info += "/jobs?filter=[NOT_STARTED] | [IN_PROGRESS] | [DONE] | [CANCELED]"
    return usage_info

@bp.route('/info', methods=["GET"])
def info_view():
    # Return list of routes
    output = {
        "info": "GET /help",
        "create new job": "POST /jobs",
        "get job by id": "GET /jobs/<job_id>",
        "get all existing jobs": "GET /jobs",
        "cancel job by id": "PATCH /jobs/cancel/<job_id>",
        "get all updated cohorts": "GET /patient/cohorts"
    }
    return jsonify(output)

# Create a new learning job and store that in the job queue database
@bp.route("/jobs", methods=['POST'])
def create_job():
    from src.models.QueueJob import QueueJob
    newQueueJob = QueueJob()
    db.session.add(newQueueJob)
    db.session.commit()

    # Check the current status of the newly created job
    status = ""
    if newQueueJob.status is 0:
        status = "NOT_STARTED"
    elif newQueueJob.status is 1:
        status = "IN_PROGRESS"
    elif newQueueJob.status is 2:
        status = "DONE"
    elif newQueueJob.status is 3:
        status = "CANCELED"

    return {
        "jobId": newQueueJob.id,
        "status": status,
        "dateCreated": newQueueJob.date_created
    }

# Retrieve a learning job from the job queue database by id
@bp.route("/jobs/<int:job_id>")
def get_job(job_id):
    from src.models.QueueJob import QueueJob
    job = QueueJob.query.get(job_id)

    # Check the current status of the newly created job
    status = ""
    if job.status is 0:
        status = "NOT_STARTED"
    elif job.status is 1:
        status = "IN_PROGRESS"
    elif job.status is 2:
        status = "DONE"
    elif job.status is 3:
        status = "CANCELED"

    return {
        "jobId": job.id,
        "status": status,
        "dateCreated": job.date_created
    }

# Retrieve a list of jobs currently in the job queue database
@bp.route("/jobs")
def get_jobs():
    from src.models.QueueJob import QueueJob
    job_filter = request.args
    # The list of jobs either filtered by status or not filtered at all
    jobs = []
    # The list of job dictionaries that will be sent as part of a response message
    jobDictList = []

    # If no arguments are provided with the url, then retrieve the list of all the jobs
    # in the database
    if len(job_filter) is 0:
        jobs = QueueJob.query.all()
    else:
        # If the number of arguments provided is not 1, then return a usage message
        if len(job_filter) > 1:
            usage_info_filter()
        # Otherwise, check if the correct argument is given, and filter the list of jobs
        # accordingly
        if str(job_filter['filter']) == "NOT_STARTED":
            jobs = QueueJob.query.filter(QueueJob.status == 0)
        elif str(job_filter['filter']) == "IN_PROGRESS":
            jobs = QueueJob.query.filter(QueueJob.status == 1)
        elif str(job_filter['filter']) == "DONE":
            jobs = QueueJob.query.filter(QueueJob.status == 2)
        elif str(job_filter['filter']) == "CANCELED":
            jobs = QueueJob.query.filter(QueueJob.status == 3)
        else:
            usage_info_filter()

    # After retrieving all of the requested jobs from the database, convert the jobs into a
    # a list of dictionaries before sending the list as a response message
    for job in jobs:
        jobDict = dict()
        jobDict['jobId'] = job.id
        if job.status is 0:
            jobDict['status'] = "NOT_STARTED"
        elif job.status is 1:
            jobDict['status'] = "IN_PROGRESS"
        elif job.status is 2:
            jobDict['status'] = "DONE"
        elif job.status is 3:
            jobDict['status'] = "CANCELED"
        jobDict['dateCreated'] = job.date_created
        jobDictList.append(jobDict)

    return build_json_response(json.dumps(jobDictList, default=str))

# Cancel a job that is not currently running
@bp.route("/jobs/cancel/<int:job_id>", methods=['PATCH'])
def cancel_job(job_id):
    from src.models.QueueJob import QueueJob
    job = QueueJob.query.get(job_id)

    # Check the current status of the job
    if job.status is 0:
        job.status = 3
        db.session.commit()

    return {
        "jobId": job.id,
        "status": 3,
        "dateCreated": job.date_created
    }

# Run the learning algorithm against the patient and categorize them
@bp.route("/patient/analyze", methods=['POST'])
def analyze_patient():
    return "Patient JSON posted to learning algorithm"

# Get all updated cohorts
@bp.route("/patient/cohorts")
def get_cohorts():
    cohorts = Cohort.query.all()
    chtList = []
    for cht in cohorts:
        chtDict = dict()
        chtDict['cohortId'] = cht.cid
        chtDict['paper'] = cht.paper
        chtDict['text'] = cht.text
        chtDict['email'] = cht.email
        chtList.append(chtDict)
    return build_json_response(json.dumps(chtList, default=str))

# Enter a new created cohort into DB (for initializing the cohorts for further use)
@bp.route("/patient/cohorts/<int:cid> <int:paper> <int:text> <int:email>", methods=['POST'])
def create_cohort(cid, paper, text, email):
    newCohort = Cohort()
    newCohort.cid = cid
    newCohort.paper = paper
    newCohort.text = text
    newCohort.email = email
    db.session.add(newCohort)
    db.session.commit()

    return {
        "cohortId": newCohort.cid,
        "freqPaper": newCohort.paper,
        "freqText": newCohort.text,
        "freqEmail": newCohort.email
    }

# Create and enter a new communication into DB
@bp.route("/communications/<int:uid>,<int:account_id>,<string:notification_date_time>,<string:method>,<string:notification_type>", methods=['POST'])
def create_communication(uid, account_id, notification_date_time, method, notification_type):
    newCom = Communication()
    newCom.uid = uid
    newCom.accountId = account_id
    newCom.notification_date_time = notification_date_time
    newCom.method = method
    newCom.notification_type = notification_type
    db.session.add(newCom)
    db.session.commit()

    return {
        "Unique ID": newCom.uid,
        "Account ID": newCom.accountId,
        "Notification Date Time": newCom.notification_date_time,
        "Delivery Method": newCom.method,
        "Notification Type": newCom.notification_type
    }
"""
# Get all current communications from DB
@bp.route("/communications")
def get_all_communications():
    coms = Communication.query.all()
    comList = []
    for com in coms:
        comDict = dict()
        comDict['accountId'] = com.accountId
        comDict['notification_date_time'] = com.notification_date_time
        comDict['method'] = com.method
        comDict['notification_type'] = com.notification_type
        comList.append(comDict)
        return build_json_response(json.dumps(comList, default=str))
"""
