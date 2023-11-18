from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# CSV file path
CSV_FILE = 'taskdb.csv'

# Function to load tasks from CSV
def load_tasks():
    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            tasks = list(reader)
        return tasks
    except FileNotFoundError:
        return []

# Function to save tasks to CSV
def save_tasks(tasks):
    with open(CSV_FILE, 'w', newline='') as file:
        fieldnames = ['id', 'name_of_staff', 'title', 'content_of_task', 'date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(tasks)

# Resource for handling task submissions
@app.route('/submit-task', methods=['POST'])
def submit_task():
    data = request.json

    # Generate task id and submission date
    task_id = len(load_tasks()) + 1
    submission_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create the new task
    new_task = {
        'id': task_id,
        'name_of_staff': data.get('name_of_staff'),
        'title': data.get('title'),
        'content_of_task': data.get('content_of_task'),
        'date': submission_date
    }

    # Load existing tasks
    existing_tasks = load_tasks()

    # Append the new task
    existing_tasks.append(new_task)

    # Save the updated tasks to the CSV file
    save_tasks(existing_tasks)

    return jsonify({'status': 'success', 'message': 'Task submitted successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
