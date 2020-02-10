from src.blueprints.core.bp import bp
from flask import request

@bp.route("/")
def hello_world():
    return "Hello World"

@bp.route("/jobs", methods=['POST'])
def create_job():
    return request.json

@bp.route("/jobs/<int:job_id>")
def get_job(job_id):
    return {
        "jobId": job_id,
        "example": "JSON",
    }