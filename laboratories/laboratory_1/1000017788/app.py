"""
Multichannel Notification System REST API
Advanced Individual Lab

This module implements a REST API for managing users and sending notifications
using design patterns including Chain of Responsibility and Singleton.
"""

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
import random
import logging
from datetime import datetime
from typing import List, Dict, Optional
from abc import ABC, abstractmethod

# Import our custom modules
from models.user import User
from models.notification import Notification
from patterns.chain_of_responsibility import NotificationChain, EmailHandler, SMSHandler, ConsoleHandler
from patterns.singleton import NotificationLogger
from patterns.strategy import NotificationStrategyContext, HighPriorityStrategy, MediumPriorityStrategy, LowPriorityStrategy
from patterns.factory import NotificationChannelFactory

app = Flask(__name__)
api = Api(app, version='1.0', title='Multichannel Notification System API',
          description='A modular REST API for managing users and sending notifications using design patterns',
          doc='/swagger/')

# Namespaces for better organization
users_ns = Namespace('users', description='User management operations')
notifications_ns = Namespace('notifications', description='Notification operations')

api.add_namespace(users_ns)
api.add_namespace(notifications_ns)

# In-memory storage
users_storage: Dict[str, User] = {}

# Initialize logger singleton
logger = NotificationLogger()

# Swagger models
user_model = api.model('User', {
    'name': fields.String(required=True, description='User name'),
    'preferred_channel': fields.String(required=True, description='Preferred notification channel', 
                                     enum=['email', 'sms', 'console']),
    'available_channels': fields.List(fields.String, required=True, 
                                    description='Available notification channels')
})

notification_model = api.model('Notification', {
    'user_name': fields.String(required=True, description='Target user name'),
    'message': fields.String(required=True, description='Notification message'),
    'priority': fields.String(required=True, description='Notification priority', 
                             enum=['high', 'medium', 'low'])
})

@users_ns.route('')
class UserList(Resource):
    @users_ns.doc('list_users')
    @users_ns.marshal_list_with(user_model)
    def get(self):
        """List all registered users"""
        return [user.to_dict() for user in users_storage.values()]
    
    @users_ns.doc('create_user')
    @users_ns.expect(user_model)
    @users_ns.marshal_with(user_model, code=201)
    def post(self):
        """Register a new user"""
        data = request.json
        
        # Validate input
        if not data or 'name' not in data:
            api.abort(400, 'Name is required')
        
        if 'preferred_channel' not in data:
            api.abort(400, 'Preferred channel is required')
        
        if 'available_channels' not in data:
            api.abort(400, 'Available channels are required')
        
        # Validate channels
        valid_channels = ['email', 'sms', 'console']
        if data['preferred_channel'] not in valid_channels:
            api.abort(400, f'Invalid preferred channel. Must be one of: {valid_channels}')
        
        for channel in data['available_channels']:
            if channel not in valid_channels:
                api.abort(400, f'Invalid channel "{channel}". Must be one of: {valid_channels}')
        
        if data['preferred_channel'] not in data['available_channels']:
            api.abort(400, 'Preferred channel must be included in available channels')
        
        # Check if user already exists
        if data['name'] in users_storage:
            api.abort(409, 'User already exists')
        
        # Create user
        user = User(
            name=data['name'],
            preferred_channel=data['preferred_channel'],
            available_channels=data['available_channels']
        )
        
        users_storage[user.name] = user
        logger.log(f"User '{user.name}' registered successfully")
        
        return user.to_dict(), 201

@notifications_ns.route('/send')
class NotificationSender(Resource):
    @notifications_ns.doc('send_notification')
    @notifications_ns.expect(notification_model)
    def post(self):
        """Send a notification to a user"""
        data = request.json
        
        # Validate input
        if not data or 'user_name' not in data:
            api.abort(400, 'User name is required')
        
        if 'message' not in data:
            api.abort(400, 'Message is required')
        
        if 'priority' not in data:
            api.abort(400, 'Priority is required')
        
        # Validate priority
        valid_priorities = ['high', 'medium', 'low']
        if data['priority'] not in valid_priorities:
            api.abort(400, f'Invalid priority. Must be one of: {valid_priorities}')
        
        # Check if user exists
        user = users_storage.get(data['user_name'])
        if not user:
            api.abort(404, 'User not found')
        
        # Create notification
        notification = Notification(
            user_name=data['user_name'],
            message=data['message'],
            priority=data['priority']
        )
        
        # Use Strategy pattern for priority handling
        strategy_context = NotificationStrategyContext()
        if data['priority'] == 'high':
            strategy_context.set_strategy(HighPriorityStrategy())
        elif data['priority'] == 'medium':
            strategy_context.set_strategy(MediumPriorityStrategy())
        else:
            strategy_context.set_strategy(LowPriorityStrategy())
        
        # Apply priority strategy
        processed_notification = strategy_context.process_notification(notification)
        
        # Create notification chain using Factory pattern
        factory = NotificationChannelFactory()
        chain = NotificationChain()
        
        # Organize channels: preferred first, then others
        ordered_channels = [user.preferred_channel]
        for channel in user.available_channels:
            if channel != user.preferred_channel:
                ordered_channels.append(channel)
        
        # Build chain
        for channel in ordered_channels:
            handler = factory.create_handler(channel)
            chain.add_handler(handler)
        
        # Process notification through chain
        result = chain.handle(processed_notification, user)
        
        return {
            'status': 'success' if result else 'failed',
            'message': 'Notification processed',
            'notification_id': processed_notification.id,
            'attempts': len(ordered_channels),
            'delivered': result
        }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
