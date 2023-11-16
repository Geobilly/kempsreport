from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS  # Import CORS
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

# CSV file path
CSV_FILE = 'users.csv'

# Function to load users from CSV
def load_users():
    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            users = list(reader)
        return users
    except FileNotFoundError:
        return []

# Authentication function
def authenticate(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user  # Return the user data if authenticated
    return None

# Resource for handling login
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username and password:
            authenticated_user = authenticate(username, password)
            if authenticated_user:
                # Only include relevant data (username and role) in the response
                response_data = {
                    'username': authenticated_user['username'],
                    'role': authenticated_user['role'],
                    'status': 'success',
                    'message': 'Login successful'
                }
                return response_data, 200
            else:
                return {'status': 'failed', 'message': 'Invalid credentials'}, 401
        else:
            return {'status': 'failed', 'message': 'Username and password are required'}, 400

# Add resource to API
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)
