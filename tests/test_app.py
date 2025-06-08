import sys
import os
import pytest
import importlib
from io import BytesIO
from dotenv import load_dotenv

# Ensure correct import path and load environment variables
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Dynamically import the Flask application
saas_app = importlib.import_module("saas-app")
app = saas_app.app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Scenario 1: Release and Remediate
# def test_scenario1_feature(client):
#     response = client.get("/scenario1/feature")
#     assert response.status_code == 200
#     data = response.get_json()
#     assert "feature_flag" in data


def test_scenario1_toggle(client):
    response = client.post("/scenario1/toggle", json={"on": True})
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data
    assert data["success"] in [True, False]


def test_scenario1_upload(client):
    data = {
        'file': (BytesIO(b'my file contents'), 'testfile.txt')
    }
    response = client.post("/scenario1/upload", content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["filename"] == 'testfile.txt'


# Scenario 2: Target
def test_scenario2_download_file(client):
    response = client.get(
        "/scenario2/download-file?email=test@example.com&region=us-west&subscription=premium&filename=testfile.txt"
    )
    assert response.status_code in [200, 403, 404]
    if response.status_code == 200:
        assert response.data
    else:
        data = response.get_json()
        assert "success" in data
        assert data["success"] is False


# Scenario 3: Experimentation
def test_scenario3_banner_clicked(client):
    response = client.post(
        "/scenario3/banner-clicked",
        json={
            "email": "test@example.com",
            "region": "us-west",
            "subscription": "premium",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "event tracked"