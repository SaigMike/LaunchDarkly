import sys
import os
import pytest
import importlib

# Adjust path explicitly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

saas_app = importlib.import_module("saas-app")
app = saas_app.app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_feature_one(client):
    response = client.get('/feature-one')
    assert response.status_code == 200
    data = response.get_json()
    assert 'feature_flag' in data

def test_landing_page(client):
    response = client.get('/landing-page?email=test@example.com&region=us-west&subscription=premium')
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['email'] == 'test@example.com'
