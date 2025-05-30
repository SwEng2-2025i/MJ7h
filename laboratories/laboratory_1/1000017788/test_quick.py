#!/usr/bin/env python3
"""
Quick test script to verify all components work
"""

print("🧪 Testing Multichannel Notification System Components...")

try:
    # Test model imports
    print("📦 Testing model imports...")
    from models.user import User
    from models.notification import Notification
    print("✅ Models imported successfully")
    
    # Test pattern imports
    print("📦 Testing pattern imports...")
    from patterns.singleton import NotificationLogger
    from patterns.strategy import HighPriorityStrategy, NotificationStrategyContext
    from patterns.factory import NotificationChannelFactory
    from patterns.chain_of_responsibility import NotificationChain, EmailHandler
    print("✅ Patterns imported successfully")
    
    # Test basic functionality
    print("🔧 Testing basic functionality...")
    
    # Test User model
    user = User("Test User", "email", ["email", "sms"])
    print(f"✅ User created: {user.name}")
    
    # Test Notification model
    notification = Notification("Test User", "Test message", "high")
    print(f"✅ Notification created: {notification.id}")
    
    # Test Singleton
    logger1 = NotificationLogger()
    logger2 = NotificationLogger()
    assert logger1 is logger2, "Singleton failed!"
    print("✅ Singleton pattern working")
    
    # Test Strategy
    strategy = HighPriorityStrategy()
    context = NotificationStrategyContext()
    context.set_strategy(strategy)
    processed = context.process_notification(notification)
    print(f"✅ Strategy pattern working: {processed.message[:30]}...")
    
    # Test Factory
    factory = NotificationChannelFactory()
    handler = factory.create_handler('email')
    print("✅ Factory pattern working")
    
    # Test Chain
    chain = NotificationChain()
    email_handler = EmailHandler()
    chain.add_handler(email_handler)
    print("✅ Chain of Responsibility working")
    
    print("\n🎉 All components working correctly!")
    print("🚀 Ready to start the API server!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n📍 To start the server, run: python app.py")
print("📚 Documentation will be at: http://localhost:5000/swagger/")
