import sys
import os
import pytest
import importlib
from dotenv import load_dotenv

# Ensure correct import path and load environment variables
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Dynamically import the Flask application
saas_app = importlib.import_module("saas-app")
app = saas_app.app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Scenario 1: Release and Remediate
def test_scenario1_feature(client):
    response = client.get('/scenario1/feature')
    assert response.status_code == 200
    data = response.get_json()
    assert 'feature_flag' in data

# Scenario 2: Target
def test_scenario2_landing_page(client):
    response = client.get('/scenario2/landing-page?email=test@example.com&region=us-west&subscription=premium')
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['email'] == 'test@example.com'
    assert 'content' in data
    assert 'feature_flag' in data

# Scenario 3: Experimentation
def test_scenario3_banner_clicked(client):
    response = client.post('/scenario3/banner-clicked', json={
        'email': 'test@example.com',
        'region': 'us-west',
        'subscription': 'premium'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'event tracked'
