from flask import Flask, jsonify
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

# Resource for handling task fetching
@app.route('/fetch-tasks', methods=['GET'])
def fetch_tasks():
    # Load all tasks
    tasks = load_tasks()

    # Return the tasks as JSON
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(debug=True)
