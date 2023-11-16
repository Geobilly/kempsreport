from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS  # Import CORS
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

# CSV file path
CSV_FILE = 'reportdb.csv'

# Function to load all reports from CSV
def load_all_reports():
    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            reports = list(reader)
        return reports
    except FileNotFoundError:
        return []

# Resource for handling report fetching
class ReportFetchResource(Resource):
    def get(self):
        # Load all reports
        reports = load_all_reports()

        # Return the reports as JSON
        return jsonify(reports)

# Add resource to API with the desired endpoint name
api.add_resource(ReportFetchResource, '/fetch-reports')

if __name__ == '__main__':
    app.run(debug=True)
