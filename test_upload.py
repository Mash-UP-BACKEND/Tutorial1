import os, io, json, filecmp
import tempfile

import pytest

from upload import upload

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

def test_upload(client):
    response = client.post("/upload")
    assert response.status_code == 400

    data = dict(file=(io.BytesIO(b"hi"), None))
    response = client.post("/upload", data=data, content_type='multipart/form-data')
    assert response.status_code == 400

    test_filename = "test.jpg"
    with open("images/brown.jpg", "rb") as img:
        data = dict(file=(img, test_filename))
        response = client.post("/upload", data=data, content_type='multipart/form-data')
        assert response.status_code == 200

        assert_json = dict(path=os.path.join(upload.create_app().config["IMAGE_DIR"], test_filename))
        response_json = json.loads(response.data)
        assert sorted(response_json.items()) == sorted(assert_json.items())

def test_image(client):
    target_filename = "images/brown.jpg"
    response = client.get(target_filename)
    assert response.status_code == 200
    assert os.path.getsize(target_filename) == len(response.data)
      

    

    

    
        
    