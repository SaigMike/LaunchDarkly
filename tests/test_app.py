# tests/test_app.py
import pytest
from saas_app import app

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
