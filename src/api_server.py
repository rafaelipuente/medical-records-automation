#!/usr/bin/env python3

import os
import json
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import logging
from datetime import datetime

# Add the current directory to the path to ensure imports work correctly
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our own modules
from data_cleaner import clean_csv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("patient_api")

# Initialize Flask app
app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

# Configuration
app.config['UPLOAD_FOLDER'] = '../uploads'
app.config['REPORTS_FOLDER'] = '../patient_reports'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Ensure directories exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True, parents=True)
Path(app.config['REPORTS_FOLDER']).mkdir(exist_ok=True)
Path("../logs").mkdir(exist_ok=True)
Path("../data").mkdir(exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    """Render the home page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Error rendering home page. Check server logs.'
        }), 500

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/upload', methods=['POST'])
def upload_patients_csv():
    """Upload a patients.csv file for processing"""
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No file part in the request'
        }), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'No file selected'
        }), 400
    
    if file and allowed_file(file.filename):
        try:
            # Create necessary directories
            os.makedirs('data', exist_ok=True)
            os.makedirs('logs', exist_ok=True)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Save the uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{filename}"
            upload_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], safe_filename))
            file.save(upload_path)
            
            logger.info(f"Saved uploaded file to {upload_path}")
            
            # Set absolute paths for the processed files
            data_dir = os.path.abspath('data')
            log_dir = os.path.abspath('logs')
            cleaned_path = os.path.join(data_dir, f"cleaned_{timestamp}.csv")
            log_path = os.path.join(log_dir, f"cleaning_{timestamp}.log")
            
            logger.info(f"Cleaning CSV from {upload_path} to {cleaned_path}")
            
            # Clean the CSV
            clean_success = clean_csv(
                input_file=upload_path,
                output_file=cleaned_path,
                log_file=log_path
            )
            
            if not clean_success:
                logger.error(f"Failed to clean CSV: {upload_path}")
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to clean CSV data. See logs for details.'
                }), 500
            
            logger.info(f"Successfully cleaned CSV to {cleaned_path}")
            
            return jsonify({
                'status': 'success',
                'message': 'File uploaded and cleaned successfully',
                'original_file': filename,
                'cleaned_file': os.path.basename(cleaned_path),
                'log_file': os.path.basename(log_path),
                'job_id': timestamp
            })
            
        except Exception as e:
            logger.error(f"Error processing upload: {e}")
            return jsonify({
                'status': 'error',
                'message': f'Error processing upload: {str(e)}'
            }), 500
    
    return jsonify({
        'status': 'error',
        'message': 'File type not allowed. Please upload a CSV file.'
    }), 400

@app.route('/api/generate-reports', methods=['POST'])
def generate_patient_reports():
    """Generate patient reports from cleaned data"""
    data = request.json
    if not data or 'job_id' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing job_id in request'
        }), 400
    
    job_id = data['job_id']
    cleaned_file = os.path.abspath(f"data/cleaned_{job_id}.csv")
    
    logger.info(f"Looking for cleaned file at: {cleaned_file}")
    if not Path(cleaned_file).exists():
        # Try alternative path
        cleaned_file = os.path.abspath(f"../data/cleaned_{job_id}.csv")
        logger.info(f"Trying alternative path: {cleaned_file}")
        
        if not Path(cleaned_file).exists():
            logger.error(f"Could not find cleaned file for job_id: {job_id}")
            return jsonify({
                'status': 'error',
                'message': f'Could not find cleaned file for job_id: {job_id}'
            }), 404
    
    # Create a job-specific output directory
    output_dir = os.path.abspath(f"{app.config['REPORTS_FOLDER']}/{job_id}")
    Path(output_dir).mkdir(exist_ok=True)
    
    try:
        logger.info(f"Generating reports from {cleaned_file} to {output_dir}")
        # Generate reports
        from report_generator import main as generate_reports
        generate_reports(
            generate_samples=False, 
            input_file=cleaned_file, 
            output_folder=output_dir
        )
        
        # Get list of generated reports
        reports = list(Path(output_dir).glob("*.pdf"))
        report_filenames = [report.name for report in reports]
        
        logger.info(f"Generated {len(reports)} reports: {report_filenames}")
        return jsonify({
            'status': 'success',
            'message': f'Generated {len(reports)} reports',
            'reports': report_filenames,
            'job_id': job_id
        })
        
    except Exception as e:
        logger.error(f"Error generating reports: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Error generating reports: {str(e)}'
        }), 500

@app.route('/api/download-report/<job_id>/<filename>')
def download_report(job_id, filename):
    """Download a specific patient report"""
    report_path = Path(f"{app.config['REPORTS_FOLDER']}/{job_id}/{secure_filename(filename)}")
    
    if not report_path.exists():
        return jsonify({
            'status': 'error',
            'message': f'Report file not found: {filename}'
        }), 404
    
    try:
        return send_file(
            report_path,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Error downloading report: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Error downloading report: {str(e)}'
        }), 500

@app.route('/api/download-cleaned-data/<job_id>')
def download_cleaned_data(job_id):
    """Download the cleaned patient data"""
    cleaned_file = Path(f"../data/cleaned_{job_id}.csv")
    
    if not cleaned_file.exists():
        return jsonify({
            'status': 'error',
            'message': f'Cleaned data file not found for job_id: {job_id}'
        }), 404
    
    try:
        return send_file(
            cleaned_file,
            as_attachment=True,
            download_name=f"cleaned_patients_{job_id}.csv"
        )
    except Exception as e:
        logger.error(f"Error downloading cleaned data: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Error downloading cleaned data: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Use environment variables for configuration in production
    port = int(os.environ.get('PORT', 8001))  # Changed default port to 8001
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
