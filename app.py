from flask import Flask
from flask_restful import Api
from flask_cors import CORS  # Import CORS
from sendreport import ReportSubmissionResource
from fetchreport import ReportFetchResource
from login import LoginResource

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

# Add resources from sendreport.py
api.add_resource(ReportSubmissionResource, '/submit-report')

# Add resources from fetchreport.py
api.add_resource(ReportFetchResource, '/fetch-reports')

# Add resource from login.py
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)
