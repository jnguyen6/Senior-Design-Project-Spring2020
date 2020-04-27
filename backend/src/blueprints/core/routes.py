from src.blueprints.core.bp import bp
from flask import request
from flask import jsonify, Response
from app import db
from src.models.Cohort import Cohort
from src.models.Communication import Communication
from src.models.WebActivity import WebActivity
from src.models.Patient import Patient
import json
from src.algorithms.categorize import categorizeFromBuckets
from datetime import date

def get_status_string(status_int):
    if status_int is 0:
        return "NOT_STARTED"
    elif status_int is 1:
        return "IN_PROGRESS"
    elif status_int is 2:
        return "DONE"
    elif status_int is 3:
        return "CANCELED"

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
@bp.route("/jobs/<string:algorithmType>", methods=['POST'])
def create_job():
    from src.models.QueueJob import QueueJob
    new_queue_job = QueueJob()
    new_queue_job.algorithm = algorithm
    db.session.add(new_queue_job)
    db.session.commit()

    # Check the current status of the newly created job
    status = ""
    if new_queue_job.status is 0:
        status = "NOT_STARTED"

    return {
        "jobId": new_queue_job.id,
        "status": status,
        "dateCreated": new_queue_job.date_created
    }

# Retrieve a learning job from the job queue database by id
@bp.route("/jobs/<int:job_id>")
def get_job(job_id):
    from src.models.QueueJob import QueueJob
    job = QueueJob.query.get(job_id)

    # Check the current status of the newly created job
    status = get_status_string(job.status)

    return {
        "jobId": job.id,
        "status": status,
        "Algorithm":job.algorithm,
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
            return Response(usage_info_filter(), status=400)
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
            return Response(usage_info_filter(), status=400)

    # After retrieving all of the requested jobs from the database, convert the jobs into a
    # a list of dictionaries before sending the list as a response message
    for job in jobs:
        jobDict = dict()
        jobDict['jobId'] = job.id
        jobDict['status'] = get_status_string(job.status)
        jobDict['jobAlgorithm'] = job.algorithm
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
        "Algorithm":job.algorithm,
        "dateCreated": job.date_created
    }

# Run the learning algorithm against the patient and categorize them
@bp.route("/patient/analyze", methods=['POST'])
def analyze_patient():
    #TODO add flag that won't let it run if not updated list of cohorts
    patient = request.get_json()

    patId = patient['id']
    cid = categorizeFromBuckets(patient)    

    return {
        "cid": cid,
        "patient": patId
    }

# Create and enter a new patient into DB
@bp.route("/patients/<int:account_id>,<string:gender>,<int:birth_year>,<string:address_zip>,<int:family_income>,<int:bill_amount>", methods=['POST'])
def create_patient(account_id, gender, birth_year, address_zip, family_income, bill_amount):
    newPatient = Patient()
    newPatient.accountId = account_id
    newPatient.gender = gender
    newPatient.birth_year = birth_year
    newPatient.address_zip = address_zip
    newPatient.family_income = family_income
    newPatient.bill_amount = bill_amount
    db.session.add(newPatient)
    db.session.commit()
    return {
        "Account ID": newPatient.accountId,
        "Gender": newPatient.gender,
        "Birth Year": newPatient.birth_year,
        "Address Zip": newPatient.address_zip,
        "Family Income": newPatient.family_income,
        "Bill Amount": newPatient.bill_amount
    }

# Get all updated cohorts
@bp.route("/patient/cohorts")
def get_cohorts():
    #TODO add database flag so that this can update status as retrieved
    cohorts = Cohort.query.all()
    
    condensedCohorts = create_cohort_list(cohorts)
    return build_json_response(json.dumps(condensedCohorts, default=str))
  

def create_cohort_list(cohorts):
    """
    Helper function for returning cohorts
    Finds all unique cycles and the returns them as a list of dictionaries
    Dict has cycle length attributes
    :param cohorts: The list of cohorts
    :return A list of dictionaries that contain all cycles in each cohort
    """
    condensedCohorts = set()
    for coh in cohorts:
        condensedCohorts.add(coh.cid)

    structuredResponse = []
    for coh in condensedCohorts:
        new_dict = dict()
        new_dict['cohortId'] = coh.cid
        new_dict['paper'] = coh.paper
        new_dict['text'] = coh.text
        new_dict['email'] = coh.email
        structuredResponse.append(new_dict)
    return structuredResponse
