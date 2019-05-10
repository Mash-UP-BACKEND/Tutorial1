import os
import tempfile

import pytest

import upload
from flask import g
@pytest.fixture
def client():
    uploader = upload.create_app()
    db_fd, uploader.config['DATABASE'] = tempfile.mkstemp()
    uploader.config['TESTING'] = True
    client = uploader.test_client()

    with uploader.app_context():
        upload.init_db(uploader.config['DATABASE'])

    yield client

    os.close(db_fd)
    os.unlink(uploader.config['DATABASE'])

def test_index(client):
    respose = client.get("/")
    assert respose.status_code == 200
    assert b'<form id="ajax-upload" action="/upload"' in respose.data


    