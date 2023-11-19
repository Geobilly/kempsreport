from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from sendreport import ReportSubmissionResource
from fetchreport import ReportFetchResource
from login import LoginResource
from submittask import submit_task
from fetchtask import fetch_tasks
from fetch_username import fetch_usernames
from updatestatus import update_status  # Import the update_status function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

# Add resource for submitting tasks
app.route('/submit-task', methods=['POST'])(submit_task)

# Add resource for fetching tasks
app.route('/fetch-tasks', methods=['GET'])(fetch_tasks)

# Add resource for fetching usernames
app.route('/fetch-usernames', methods=['GET'])(fetch_usernames)

# Add resource for updating task status
app.route('/update-status/<int:task_id>', methods=['PUT'])(update_status)

# Add resources from sendreport.py
api.add_resource(ReportSubmissionResource, '/submit-report')

# Add resources from fetchreport.py
api.add_resource(ReportFetchResource, '/fetch-reports')

# Add resource from login.py
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)
