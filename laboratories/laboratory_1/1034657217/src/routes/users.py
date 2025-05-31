# routes/user_routes.py
from flask_restx import Resource, fields
from utils.logger import Logger
from model.user import User as EUser 
from model.usersModel import UsersModel # Asegúrate de que esta importación exista

user_ns = None 

def init_user_routes(api_instance, users_model_instance_param): # Ahora recibe la INSTANCIA del UsersModel
    """
    Inicializa las rutas de usuario y los modelos de Flask-RestX.
    Debe ser llamado desde app.py.
    """
    global user_ns
    user_ns = api_instance.namespace('users', description='User operations')

    user_model = api_instance.model('User', {
        'name': fields.String(required=True, description='The user\'s name'),
        'preferred_channel': fields.String(required=True, enum=['email', 'sms', 'console'], description='User\'s preferred notification channel'),
        'available_channels': fields.List(fields.String(enum=['email', 'sms', 'console']), required=True, description='List of channels available for the user')
    })

    @user_ns.route('/')
    class UserList(Resource):
        @user_ns.doc('list_users')
        @user_ns.marshal_list_with(user_model)
        def get(self):
            """List all registered users"""
            # Accede a los usuarios a través de la instancia del Singleton
            return users_model_instance_param.showAllUsers(), 200 # Usa el método showAllUsers del UsersModel

        @user_ns.doc('register_user')
        @user_ns.expect(user_model, validate=True)
        @user_ns.marshal_with(user_model, code=201)
        @user_ns.response(400, 'Validation Error')
        @user_ns.response(409, 'User Already Exists')
        def post(self):
            """Register a new user"""
            data = user_ns.payload
            name = data.get('name')
            
            # Accede a los usuarios a través de la instancia del Singleton
            if users_model_instance_param.find_user_by_name(name): # Usa el método find_user_by_name
                Logger().log(f"Attempted to register existing user: {name}")
                user_ns.abort(409, "User already exists")

            users_model_instance_param.addUser(data) # Usa el método addUser para añadir el usuario
            
            Logger().log(f"User registered: {name}")
            return users_model_instance_param.lastUser(), 201 # Devuelve el último usuario añadido, desde el modelo
    
    return user_ns