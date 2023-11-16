from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS  # Import CORS
import csv
from datetime import datetime
from uuid import uuid4

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

# CSV file path
CSV_FILE = 'reportdb.csv'

# Function to load existing reports from CSV
def load_reports():
    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            reports = list(reader)
        return reports
    except FileNotFoundError:
        return []

# Function to save reports to CSV
def save_reports(reports):
    with open(CSV_FILE, 'w', newline='') as file:
        fieldnames = ['report_id', 'report_title', 'author_name', 'report_content', 'submission_date', 'attachments']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(reports)

# Resource for handling report submissions
class ReportSubmissionResource(Resource):
    def post(self):
        data = request.get_json()

        # Generate report_id and submission_date
        report_id = str(uuid4())[:8]  # Use a portion of the UUID as a unique identifier
        submission_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create the new report
        new_report = {
            'report_id': report_id,
            'report_title': data.get('report_title'),
            'author_name': data.get('author_name'),
            'report_content': data.get('report_content'),
            'submission_date': submission_date,
            'attachments': data.get('attachments')
        }

        # Load existing reports
        existing_reports = load_reports()

        # Remove empty rows (if any)
        existing_reports = [report for report in existing_reports if any(report.values())]

        # Append the new report
        existing_reports.append(new_report)

        # Save the updated reports to the CSV file
        save_reports(existing_reports)

        return {'status': 'success', 'message': 'Report submitted successfully'}, 201

# Add resource to API with the desired endpoint name
api.add_resource(ReportSubmissionResource, '/submit-report')

if __name__ == '__main__':
    app.run(debug=True)
