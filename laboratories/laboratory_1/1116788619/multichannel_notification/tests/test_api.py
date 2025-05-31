import pytest
from app import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post('/users', json={
        "name": "TestUser",
        "preferred_channel": "email",
        "available_channels": ["email", "sms"]
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully."

def test_list_users(client):
    client.post('/users', json={
        "name": "TestUser2",
        "preferred_channel": "sms",
        "available_channels": ["sms"]
    })
    response = client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert any(user["name"] == "TestUser2" for user in data)

def test_send_notification_success(client):
    # Registrar usuario
    client.post('/users', json={
        "name": "NotifyUser",
        "preferred_channel": "email",
        "available_channels": ["email", "sms"]
    })

    response = client.post('/notifications/send', json={
        "user_name": "NotifyUser",
        "message": "Testing notification",
        "priority": "alta"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "Notification attempt finished via" in data["message"]

def test_send_notification_user_not_found(client):
    response = client.post('/notifications/send', json={
        "user_name": "NonExistent",
        "message": "Testing",
        "priority": "alta"
    })
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "User not found"

def test_get_logs(client):
    response = client.get('/logs')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)