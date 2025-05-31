import pytest
from services.notification_service import NotificationService
from channels.notification_channels import EmailChannel, SMSChannel, ConsoleChannel

@pytest.fixture
def notification_service():
    return NotificationService()

def test_register_user(notification_service):
    result = notification_service.register_user(
        "test_user",
        "email",
        ["email", "sms"]
    )
    assert result == True
    
    users = notification_service.get_users()
    assert len(users) == 1
    assert users[0]["name"] == "test_user"
    assert users[0]["preferred_channel"] == "email"
    assert users[0]["available_channels"] == ["email", "sms"]

def test_register_user_invalid_channel(notification_service):
    result = notification_service.register_user(
        "test_user",
        "invalid",
        ["invalid"]
    )
    assert result == False

def test_register_user_preferred_not_in_available(notification_service):
    result = notification_service.register_user(
        "test_user",
        "email",
        ["sms"]
    )
    assert result == False

def test_send_notification_user_not_found(notification_service):
    result = notification_service.send_notification(
        "nonexistent_user",
        "test message",
        "high"
    )
    assert result == False

def test_send_notification(notification_service):
    notification_service.register_user(
        "test_user",
        "console",  # Using console as it always succeeds
        ["console"]
    )
    
    result = notification_service.send_notification(
        "test_user",
        "test message",
        "high"
    )
    assert result == True
