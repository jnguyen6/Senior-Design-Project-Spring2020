from src.blueprints.core.bp import bp
from flask import request
from flask import jsonify, Response
from app import db
from src.models.Cohort import Cohort
import json

def build_json_response(obj):
    return Response(obj, content_type='application/json')

@bp.route("/")
def hello_world():
    return "Hello World"

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
        status = "CANCELLED"

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
        status = "CANCELLED"

    return {
        "jobId": job.id,
        "status": job.status,
        "dateCreated": job.date_created
    }

# Retrieve a list of jobs currently in the job queue database
@bp.route("/jobs")
def get_jobs():
    from src.models.QueueJob import QueueJob
    jobs = QueueJob.query.all()
    jobList = []
    for job in jobs:
        jobDict = dict()
        jobDict['jobId'] = job.id
        jobDict['status'] = job.status
        jobDict['dateCreated'] = job.date_created
        jobList.append(jobDict)
    return build_json_response(json.dumps(jobList, default=str))

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
        "status": job.status,
        "dateCreated": job.date_created
    }

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

