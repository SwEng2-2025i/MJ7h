from flask_restx import Resource, fields
from app.api.namespaces import user_ns
from app.services.user_service import UserService

user_service = UserService()

user_model = user_ns.model('User', {
    'name': fields.String(required=True, description='User name'),
    'preferred_channel': fields.String(required=True, description='Preferred channel'),
    'available_channels': fields.List(fields.String, required=True, description='Available channels')
})

@user_ns.route('') 
class UserList(Resource):
    @user_ns.doc('list_users')
    def get(self):
        """List all users"""
        return user_service.get_all_users()

    @user_ns.doc('create_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model)
    def post(self):
        data = user_ns.payload
        user = user_service.register_user(
            name=data['name'],
            preferred_channel=data['preferred_channel'],
            available_channels=data['available_channels']
        )
        return user, 201  # Devuelve el usuario con su ID
        
    @user_ns.doc('list_users')
    @user_ns.response(200, 'Success')
    def get(self):
        """List all users"""
        return user_service.get_all_users()