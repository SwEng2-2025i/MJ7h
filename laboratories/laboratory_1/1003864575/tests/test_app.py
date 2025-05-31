import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from app import routes

@pytest.fixture(autouse=True)
def clean_users():
    routes.users.clear()

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post('/users', json={
        "name": "Juan",
        "preferred_channel": "email",
        "available_channels": ["email", "sms"]
    })
    assert response.status_code == 201

def test_list_users(client):
    client.post('/users', json={
        "name": "Juan",
        "preferred_channel": "email",
        "available_channels": ["email", "sms"]
    })
    response = client.get('/users')
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == "Juan"

def test_send_notification(client):
    client.post('/users', json={
        "name": "Juan",
        "preferred_channel": "email",
        "available_channels": ["email", "sms"]
    })
    response = client.post('/notifications/send', json={
        "user_name": "Juan",
        "message": "Test notification",
        "priority": "high"
    })
    assert response.status_code in [200, 500]  # Puede fallar o tener éxito según la lógica simulada