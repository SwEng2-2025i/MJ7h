"""
Example usage script for the notification system
Demonstrates API endpoints and functionality
"""

import requests
import json
import time

# Configuration
BASE_URL = 'http://localhost:5000'
HEADERS = {'Content-Type': 'application/json'}

def test_api():
    """
    Test the notification system API
    """
    print("🚀 Testing Multichannel Notification System API")
    print("=" * 50)
    
    # Test 1: Register users
    print("\n1. Registering users...")
    
    users = [
        {
            "name": "Juan",
            "preferred_channel": "email",
            "available_channels": ["email", "sms"]
        },
        {
            "name": "Maria",
            "preferred_channel": "sms",
            "available_channels": ["sms", "console"]
        },
        {
            "name": "Carlos",
            "preferred_channel": "email",
            "available_channels": ["email", "sms", "console"]
        }
    ]
    
    for user in users:
        try:
            response = requests.post(f"{BASE_URL}/users", 
                                   headers=HEADERS, 
                                   data=json.dumps(user))
            if response.status_code == 201:
                print(f"✅ User '{user['name']}' registered successfully")
            else:
                print(f"❌ Failed to register user '{user['name']}': {response.text}")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error. Make sure the server is running on localhost:5000")
            return
    
    # Test 2: List users
    print("\n2. Listing all users...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            users_list = response.json()
            print(f"✅ Found {len(users_list)} users:")
            for user in users_list:
                print(f"   - {user['name']} (preferred: {user['preferred_channel']})")
        else:
            print(f"❌ Failed to list users: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return
    
    # Test 3: Send notifications
    print("\n3. Sending notifications...")
    
    notifications = [
        {
            "user_name": "Juan",
            "message": "Your appointment is tomorrow at 3 PM",
            "priority": "high"
        },
        {
            "user_name": "Maria",
            "message": "Weekly newsletter available",
            "priority": "low"
        },
        {
            "user_name": "Carlos",
            "message": "System maintenance scheduled for tonight",
            "priority": "medium"
        }
    ]
    
    for notification in notifications:
        try:
            response = requests.post(f"{BASE_URL}/notifications/send",
                                   headers=HEADERS,
                                   data=json.dumps(notification))
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Notification sent to {notification['user_name']}: {result['status']}")
                print(f"   📧 Delivered: {result['delivered']}, Attempts: {result['attempts']}")
            else:
                print(f"❌ Failed to send notification to {notification['user_name']}: {response.text}")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error")
            return
        
        # Small delay between notifications
        time.sleep(1)
    
    print("\n4. API Documentation available at: http://localhost:5000/swagger/")
    print("\n✅ API testing completed!")

if __name__ == '__main__':
    test_api()
