from src.blueprints.views.bp import bp
from flask import request
from flask import render_template
from app import db
from src.models.QueueJob import QueueJob
from src.models.QueueStatus import QueueStatus

# show the landing page view when accessing the app
@bp.route("/")
def index():
    return render_template('index.html')

# Retrieve a list of jobs currently in the job queue database
@bp.route("/view/jobs")
def get_jobs():
    jobs = QueueJob.query.all()
    jobList = []
    for job in jobs:
        jobDict = dict()
        jobDict['job ID'] = job.id
        jobDict['status'] = get_status(job.status)
        jobDict['date created'] = get_pretty_date(job.date_created)
        jobList.append(jobDict)
    return render_template('table.html', jobs=jobList)

def get_status(key):

    return QueueStatus(key).name

def get_pretty_date(oldDate):

    return oldDate.strftime("%d %b %Y at %H:%M")
