import sys
import os
import pytest
import importlib
from io import BytesIO
from dotenv import load_dotenv

# Include parent directory in system path and load environment variables
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Dynamically import the Flask application from 'saas-app.py'
saas_app = importlib.import_module("saas-app")
app = saas_app.app


# Pytest fixture providing a Flask test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Test feature flag toggling for Scenario 1
def test_scenario1_toggle(client):
    response = client.post("/scenario1/toggle", json={"on": True})
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("success") in [True, False]


# Test file upload functionality for Scenario 1
def test_scenario1_upload(client):
    data = {"file": (BytesIO(b"my file contents"), "testfile.txt")}
    response = client.post(
        "/scenario1/upload", content_type="multipart/form-data", data=data
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data.get("success") is True
    assert json_data.get("filename") == "testfile.txt"


# Test file download functionality with LaunchDarkly targeting rules for Scenario 2
def test_scenario2_download_file(client):
    response = client.get(
        "/scenario2/download-file?email=test@example.com&region=us-west&subscription=premium&filename=testfile.txt"
    )
    assert response.status_code in [200, 403, 404]
    if response.status_code == 200:
        assert response.data  # Confirm file content is returned
    else:
        data = response.get_json()
        assert data.get("success") is False


# Test banner click tracking functionality for experimentation in Scenario 3
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
    assert data.get("status") == "event tracked"
