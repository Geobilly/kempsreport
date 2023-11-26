from flask import Flask, jsonify, request
from flask_cors import CORS
import csv

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

        # Filter out empty rows
        tasks = [task for task in tasks if any(task.values())]

        # Update "status" column to "Not Started" for empty rows
        for task in tasks:
            if not task.get('status'):
                task['status'] = 'Not Started'

        return tasks
    except FileNotFoundError:
        return []

# Function to save tasks to CSV
def save_tasks(tasks):
    with open(CSV_FILE, 'w', newline='') as file:
        fieldnames = ['id', 'name_of_staff', 'title', 'content_of_task', 'date', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(tasks)

# Resource for handling task fetching
@app.route('/fetch-tasks', methods=['GET'])
def fetch_tasks():
    # Load all tasks
    tasks = load_tasks()

    # Return the tasks as JSON
    return jsonify(tasks)

# Resource for updating task status
@app.route('/update-status/<int:task_id>', methods=['PUT'])
def update_status(task_id):
    # Load all tasks
    tasks = load_tasks()

    # Find the task with the specified ID
    task_to_update = next((task for task in tasks if task['id'] == str(task_id)), None)

    if task_to_update:
        new_status = request.json.get('new_status')

        # Update the task's status
        task_to_update['status'] = new_status

        # Save the updated tasks to the CSV file
        save_tasks(tasks)

        return jsonify({'status': 'success', 'message': f'Status of task {task_id} updated to {new_status}'}), 200
    else:
        return jsonify({'status': 'failed', 'message': f'Task with ID {task_id} not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
