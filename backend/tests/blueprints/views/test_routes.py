import json
import pytest

def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type

def test_get_jobs(client):
    client.post('/jobs')
    resp = client.get('/view/jobs')
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type

def test_get_cohort_by_user_stats(client):
    resp = client.get('/view/user')
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type

    resp = client.post("/view/user")
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type

def test_get_cohorts_view(client):
    resp = client.get('/view/cohorts')
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type

def test_get_by_cohort_id(client):
    resp = client.get('/view/cohorts/1')
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type
