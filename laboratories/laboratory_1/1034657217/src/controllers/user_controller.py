from flask import jsonify, request
from model import usersModel

class UserController:
    def __init__(self):
        self.user_model = usersModel.UsersModel()


    def get_all_users(self):
       try:
            #lista de los usuarios
           allUsers=self.user_model.showAllUsers()
           return jsonify({
                   'users':allUsers, 
                   'success':True,
               }), 200
       except Exception as e:
           return jsonify({
                "success": False,
                "error": str(e)
                }), 500
    
    def register_user(self):
        try:
            if request.is_json:
                data = request.get_json()
                name= data.get("name")
                preferred_channel= data.get("preferred_channel")
                available_channels=data.get("available_channels")
            #crear diccionario con datos del nuevo usuario
            newUser = {"name":name,"preferred_channel":preferred_channel,"available_channels":available_channels}

            self.user_model.addUser(newUser)
            return jsonify({
                   'success':True,
                   'user_created': self.user_model.lastUser()
               }), 200
        except Exception as e:
            return jsonify({
                "success":False,
                "error":str(e)
            }), 500
       