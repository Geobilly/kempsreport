from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from datetime import datetime
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# CSV file paths
TASKS_FILE = 'taskdb.csv'
USERS_FILE = 'users.csv'

# Function to load tasks from CSV
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            reader = csv.DictReader(file)
            tasks = list(reader)
        return tasks
    except FileNotFoundError:
        return []

# Function to load users from CSV
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            reader = csv.DictReader(file)
            users = {user['username']: user['number'] for user in reader}
        return users
    except FileNotFoundError:
        return {}

# Function to save tasks to CSV
def save_tasks(tasks):
    with open(TASKS_FILE, 'w', newline='') as file:
        fieldnames = ['id', 'name_of_staff', 'title', 'content_of_task', 'date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(tasks)

# Function to send SMS
def send_sms(to_number, message_body):
    # Hubtel SMS API configuration
    HUBTEL_API_URL = 'https://smsc.hubtel.com/v1/messages/send'
    HUBTEL_CLIENT_ID = 'uppxidtz'
    HUBTEL_CLIENT_SECRET = 'khhmovbe'

    params = {
        'clientsecret': HUBTEL_CLIENT_SECRET,
        'clientid': HUBTEL_CLIENT_ID,
        'from': 'YourSenderID',  # Replace with your sender ID
        'to': to_number,
        'content': message_body
    }

    try:
        # Send SMS via Hubtel API
        response = requests.get(HUBTEL_API_URL, params=params)

        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('status') == 0:
                return True
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")

    return False

# Resource for handling task submissions
@app.route('/submit-task', methods=['POST'])
def submit_task():
    data = request.json

    # Generate task id and submission date
    task_id = len(load_tasks()) + 1
    submission_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Load existing tasks and users
    existing_tasks = load_tasks()
    users = load_users()

    # Retrieve the phone number based on the selected staff's username
    username = data.get('name_of_staff')
    to_number = users.get(username)

    if to_number:
        # Create the new task
        new_task = {
            'id': task_id,
            'name_of_staff': username,
            'title': data.get('title'),
            'content_of_task': data.get('content_of_task'),
            'date': submission_date
        }

        # Append the new task
        existing_tasks.append(new_task)

        # Save the updated tasks to the CSV file
        save_tasks(existing_tasks)

        # Send SMS
        link = 'http://bit.ly/3SZgiLI'  # Replace with your actual link
        message_body = f"New task assigned: {data.get('title')}. Visit {link} for more details"
        if send_sms(to_number, message_body):
            return jsonify({'status': 'success', 'message': 'Task submitted successfully. SMS sent successfully'}), 201
        else:
            return jsonify({'status': 'success', 'message': 'Task submitted successfully. Failed to send SMS.'}), 201

    else:
        return jsonify({'status': 'error', 'message': 'User not found or phone number not available'}), 404

if __name__ == '__main__':
    app.run(debug=True)
