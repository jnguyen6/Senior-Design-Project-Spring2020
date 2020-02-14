import json
import pytest
from src.models.QueueJob import QueueStatus

@pytest.fixture
def queue_shape():
    return dict(id=0, status="", date_created="").keys()

def test_create_job(client, queue_shape):
    resp = client.post('/jobs')
    assert resp.status_code == 200

    assert json.loads(resp.data).keys() == queue_shape

def test_get_all_jobs(client, queue_shape):
    resp = client.get('/jobs')
    assert resp.status_code == 200

    data_list = json.loads(resp.data)
    assert type(data_list) == list

    if len(data_list) > 0:
        assert data_list[0].keys() == queue_shape

def test_get_job_by_id(client, queue_shape):
    new_job = json.loads(client.post('/jobs'))
    resp = client.get(f'/jobs/{new_job["id"]}')
    assert resp.status_code == 200

    resp_json = json.loads(resp.data)
    assert resp_json.keys() == queue_shape

    assert resp_json["id"] == new_job["id"]

def test_get_job_by_id_fail(client):
    resp = client.get(f'/jobs/{-1}')
    assert resp.status_code == 404

def test_cancel_job(client, queue_shape):
    new_job = json.loads(client.post('/jobs'))
    resp = client.patch(f'/jobs/cancel/{new_job["id"]}')
    assert resp.status_code == 200

    resp_json = json.loads(resp.data)
    assert resp_json.keys() == queue_shape

    assert resp_json["id"] == new_job["id"]

    assert resp_json["status"] == QueueStatus.CANCELLED

def test_analyze_patient(client):
    patient = dict(
        account_id = 1,
        date_of_birth = "",
        gender = "m",
        income = 20000,
        bill = 500
    )
    resp = client.post('/patient/analyze', data=json.dumps(patient))
    assert resp.status_code == 200
    # TODO Test the expected outputs of this endpoint

def test_get_cohorts(client):
    resp = client.get('/patient/cohorts')
    assert resp.status_code == 200

    resp_json = json.loads(resp.data)
    assert type(resp_json) == list
    # TODO test the content of this list

