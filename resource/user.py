import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username is required")
    parser.add_argument('password', type=str, required=True, help="Password is required")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400

        new_user = UserModel(data['username'], data['password'])
        new_user.save_to_db()

        return {"message": "User created successfully."}, 201

class Users(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        users = []
        query = "SELECT * FROM users"
        results = cursor.execute(query)
        if results:
            for row in results:
                users.append({'_id': row[0], 'username': row[1]})
            return {'users': users}, 200
        return {'message': 'No users found'}, 400
