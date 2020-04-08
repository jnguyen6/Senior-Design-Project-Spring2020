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