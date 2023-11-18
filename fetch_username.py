from flask import Flask, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# CSV file path for users
USERS_CSV_FILE = 'users.csv'

# Function to fetch all usernames from CSV
def fetch_usernames():
    try:
        with open(USERS_CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            usernames = [row['username'] for row in reader]
        return usernames
    except FileNotFoundError:
        return []

# Resource for fetching all usernames
@app.route('/fetch-usernames', methods=['GET'])
def fetch_usernames_route():
    # Load all usernames
    usernames = fetch_usernames()

    # Return the usernames as JSON
    return jsonify(usernames)

if __name__ == '__main__':
    app.run(debug=True)
