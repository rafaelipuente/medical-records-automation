# Patient Data Automation

[![GitHub](https://img.shields.io/badge/View_on-GitHub-blue)](https://github.com/rafaelipuente/medical-records-automation)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This project provides a comprehensive solution for healthcare data management, from data cleaning to professional report generation. It standardizes patient information, generates professional PDF reports, and provides both CLI and web interfaces for easy data processing.

![Patient Data Web Interface](https://via.placeholder.com/800x400?text=Patient+Data+Web+Interface)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/rafaelipuente/medical-records-automation.git

# Navigate to the project directory
cd medical-records-automation

# Install dependencies
pip install -r requirements.txt

# Run the web interface
python src/api_server.py
```

Then open your browser to http://localhost:8001 to access the web interface.

---

## ✨ Features

### Data Cleaning & Validation
- Standardizes patient names, dates, phone numbers, and email formats
- Validates required fields and detects data inconsistencies
- Normalizes phone numbers to the format (XXX) XXX-XXXX
- Handles different column formats (supports both 'name' and 'full_name')

### Professional Report Generation
- Creates individual PDF reports for each patient
- Includes patient information, vitals, diagnosis, and recommendations
- Generates data visualizations of vital signs
- Organized sections with headers and consistent formatting

### Web Interface
- User-friendly web interface for uploading and processing data
- Three-step workflow: Upload, Process, Download
- Bulk download options for all reports or individual selections
- Real-time processing status updates

### API Server
- RESTful API endpoints for programmatic access
- Upload patient data via POST requests
- Generate reports through API calls
- Download reports and cleaned data programmatically

### Command-Line Interface
- Flexible CLI arguments for all scripts
- Customizable input/output paths
- Demo mode for testing without sending emails
- Comprehensive logging options

---

## 📁 Project Structure

```
patient_data_automation/
├── data/                         # Data directory
│   ├── patients.csv              # Raw input data
│   └── cleaned_*.csv             # Cleaned output data with job IDs
│
├── logs/                         # Logging directory
│   └── cleaning_*.log            # Logs of processing with timestamps
│
├── patient_reports/              # Generated PDF reports
│   └── [job_id]/                 # Job-specific report directories
│
├── uploads/                      # Temporary storage for uploaded files
│
├── src/
│   ├── api_server.py             # Flask web server and API endpoints
│   ├── data_cleaner.py           # Data cleaning and validation
│   ├── report_generator.py       # PDF report generation
│   ├── email_sender.py           # Email automation
│   └── run_all.py                # One-command workflow automation
│
├── templates/                    # HTML templates for web interface
│   └── index.html                # Main web interface template
│
├── tests/                        # Unit tests
│   ├── test_data_cleaner.py      # Tests for data cleaning
│   ├── test_email_sender.py      # Tests for email functionality
│   └── test_reports.py           # Tests for report generation
│
├── README.md                     # Project documentation
├── requirements.txt              # Python package dependencies
├── Procfile                      # Deployment configuration
├── DEPLOY.md                     # Deployment instructions
└── .gitignore                    # Git exclusions
```

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.8 or higher
- Modern web browser (for web interface)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rafaelipuente/medical-records-automation.git
   cd medical-records-automation
   ```

2. **Set up a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories**
   ```bash
   mkdir -p uploads data logs patient_reports
   ```

### Usage Options

#### 1. Web Interface (Recommended)

```bash
python src/api_server.py
```

Then open your browser to http://localhost:8001 and follow the three-step process:
1. Upload your CSV file
2. Generate reports
3. Download individual or bulk reports

#### 2. Command Line Interface

**Clean data only:**
```bash
python src/data_cleaner.py -i path/to/input.csv -o path/to/output.csv
```

**Generate reports:**
```bash
python src/report_generator.py -i path/to/cleaned_data.csv -o output_folder
```

**Generate sample data for testing:**
```bash
python src/report_generator.py --generate
```

**Run the entire pipeline:**
```bash
python src/run_all.py --all
```

---

## 📋 Input File Format

The input CSV file should contain the following columns:

```csv
patient_id,full_name,date_of_birth,age,phone,email,gender,vitals_notes,blood_pressure,heart_rate,temperature,diagnosis
```

Sample data:

```csv
P001,John Doe,1985-02-01,39,555-1234,john.doe@example.com,Male,High Blood Pressure,145/95,78,36.9,Hypertension
P002,Jane Smith,1990-07-24,34,555-2345,jane.smith@example.com,Female,Normal,120/80,72,36.7,Diabetes
P003,Bob Johnson,1947-11-10,77,555-3456,bob.johnson@example.com,Male,Arthritis,121/87,64,36.6,Arthritis
```

**Note:** The system is flexible and can handle variations in column names and formats. For example, it works with both `name` and `full_name` columns.

---

## ✅ Implemented Features

- [x] Professional PDF report generation with patient vitals and charts
- [x] Command-line interface with customizable parameters
- [x] Web interface for easy data processing
- [x] RESTful API for programmatic access
- [x] Comprehensive unit testing
- [x] Robust error handling and validation
- [x] Support for both column name formats (`name` and `full_name`)

## 🔮 Future Enhancements

- [ ] User authentication for the web interface
- [ ] Analytics dashboard for patient data
- [ ] Mobile-responsive design improvements
- [ ] Additional report templates and customization options
- [ ] Export to other formats (XLSX, JSON)
- [ ] Integration with electronic health record (EHR) systems

---

## 👨‍💻 Author

Developed by Rafael Puente — Computer Science student and aspiring healthcare IT specialist.

---

## 📄 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software with appropriate attribution.

## 📬 Contact & Support

- **GitHub**: [rafaelipuente](https://github.com/rafaelipuente)
- **Project Issues**: For help or to report bugs, please [open an issue](https://github.com/rafaelipuente/medical-records-automation/issues)

---

## 📸 Screenshots

### Web Interface
![Web Interface](https://via.placeholder.com/800x400?text=Web+Interface+Screenshot)

### Sample Report
![Sample Report](https://via.placeholder.com/400x600?text=Sample+PDF+Report)

### Data Cleaning Process
![Data Cleaning](https://via.placeholder.com/800x300?text=Data+Cleaning+Visualization)

