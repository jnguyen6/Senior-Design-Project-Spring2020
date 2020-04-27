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
    
    condensedCohorts = createCohortList(cohorts)
    return build_json_response(json.dumps(condensedCohorts, default=str))
  
"""
Helper function for returning cohorts
Finds all unique cycles and the returns them as a list of dictionaries
Dict has cycle length attributes
"""
def createCohortList(cohorts):
    condensedCohorts = set()
    for coh in cohorts:
        condensedCohorts.add(coh.cid)

    structuredResponse = []
    for coh in condensedCohorts:
        newdict = dict()
        newdict['cohortId'] = coh.cid
        newdict['paper'] = coh.paper
        newdict['text'] = coh.text
        newdict['email'] = coh.email
        structuredResponse.append(newdict)
    return structuredResponse

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
        comDict['uid'] = com.uid
        comDict['accountId'] = com.accountId
        comDict['notification_date_time'] = com.notification_date_time
        comDict['method'] = com.method
        comDict['notification_type'] = com.notification_type
        comList.append(comDict)
        return build_json_response(json.dumps(comList, default=str))
"""

# Create and enter new web activity to DB
@bp.route("/web activities/<int:uid>,<int:account_id>,<int:event_id>,<string:bill_status>,<string:action_date>", methods=['POST'])
def create_web_activity(uid, account_id, event_id, bill_status, action_date):
    newWebActivity = WebActivity()
    newWebActivity.uid = uid
    newWebActivity.accountId = account_id
    newWebActivity.eventId = event_id
    newWebActivity.billStatus = bill_status
    newWebActivity.actionDate = action_date
    db.session.add(newWebActivity)
    db.session.commit()

    return {
        "Unique ID": newWebActivity.uid,
        "Account ID": newWebActivity.accountId,
        "Event ID": newWebActivity.eventId,
        "Bill Status": newWebActivity.billStatus,
        "Action Date": newWebActivity.actionDate
    }

# Get birth year of all patients
@bp.route("/patients/birth_year", methods=['GET'])
def get_patients_birth_year():
    from src.models.Patient import Patient
    patients = Patient.query.all()
    birthYearList = []
    for patient in patients:
        birthYearList.append(patient.birth_year)
    return build_json_response(json.dumps(birthYearList, default=str))

# Get gender of all patients
@bp.route("/patients/gender", methods=['GET'])
def get_patients_gender():
    from src.models.Patient import Patient
    patients = Patient.query.all()
    genderList = []
    for patient in patients:
        genderList.append(patient.gender)
    return build_json_response(json.dumps(genderList, default=str))

# Get family income of all patients
@bp.route("/patients/family_income", methods=['GET'])
def get_patients_family_income():
    from src.models.Patient import Patient
    patients = Patient.query.all()
    incomeList = []
    for patient in patients:
        incomeList.append(patient.family_income)
    return build_json_response(json.dumps(incomeList, default=str))

# Get bill amount of all patients
@bp.route("/patients/bill_amount", methods=['GET'])
def get_patients_bill_amount():
    from src.models.Patient import Patient
    patients = Patient.query.all()
    billList = []
    for patient in patients:
        billList.append(patient.bill_amount)
    return build_json_response(json.dumps(billList, default=str))

# Get account id of all patients (for iterating patient list and assign communication frequency variable)
@bp.route("/patients/account_id", methods=['GET'])
def get_patients_account_id():
    from src.models.Patient import Patient
    patients = Patient.query.all()
    idList = []
    for patient in patients:
        idList.append(patient.accountId)
    return build_json_response(json.dumps(idList, default=str))

# Get all communications
@bp.route("/communications", methods=['GET'])
def get_all_communications():
    from src.models.Communication import Communication
    coms = Communication.query.all()
    comList = []
    for com in coms:
        comDict = dict()
        comDict['uid'] = com.uid
        comDict['account_id'] = com.accountId
        comDict['notification_date_time'] = com.notification_date_time
        comDict['method'] = com.method
        comDict['notification_type'] = com.notification_type
        comList.append(comDict)
    return build_json_response(json.dumps(comList, default=str))

# Get all website activities
@bp.route("/web activities", methods=['GET'])
def get_all_web_activities():
    from src.models.WebActivity import WebActivity
    webActs = WebActivity.query.all()
    webActList = []
    for webAct in webActs:
        webActDict = dict()
        webActDict['uid'] = webAct.uid
        webActDict['account_id'] = webAct.accountId
        webActDict['eventId'] = webAct.eventId
        webActDict['billStatus'] = webAct.billStatus
        webActDict['actionDate'] = webAct.actionDate
        webActList.append(webActDict)
    return build_json_response(json.dumps(webActList, default=str))