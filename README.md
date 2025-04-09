# Patient Data Automation

This project provides a Python-based solution for cleaning, validating, and processing raw patient data for use in healthcare systems or analytical workflows. It standardizes inconsistent data entries, flags issues, and outputs both clean datasets and supporting logs. The codebase is modular and extensible, supporting additional functionality like report generation and email automation.

---

## Features

### Data Cleaning
- Standardizes patient names to title case
- Converts mixed date formats to ISO standard (YYYY-MM-DD)
- Normalizes phone numbers to the format (XXX) XXX-XXXX
- Validates and standardizes email addresses
- Harmonizes gender values (e.g., "m", "M", "Male" → "Male")

### Data Validation
- Verifies presence of required fields (patient ID, name, DOB, gender)
- Detects duplicate entries based on name and date of birth
- Validates age against date of birth with a 1-year margin of error
- Flags vital sign inconsistencies (e.g., high blood pressure in minors)

### Output and Logging
- Generates a cleaned version of the patient data as a CSV
- Logs all issues found during validation in a plain text file
- Tags each patient record as "Clean" or "Needs Review"

### Extensibility
- Designed to support modular enhancements such as:
  - PDF report generation
  - Email notifications with attachments
  - CLI argument parsing
  - Unit testing with Python’s unittest module
  - REST API integration with FastAPI

---

## Project Structure

```
patient_data_automation/
├── data/
│   ├── patients.csv              # Raw input data
│   └── cleaned_patients.csv      # Cleaned output data
│
├── logs/
│   └── data_cleaning_log.txt     # Log of issues and validation notes
│
├── patient_reports/              # Generated PDF reports (optional)
│
├── src/
│   ├── data_cleaner.py           # Main script for cleaning and validation
│   ├── report_generator.py       # PDF generation logic (optional)
│   └── email_sender.py           # Email automation (optional)
│
├── tests/                        # Unit tests
│   └── test_reports.py
│
├── README.md                     # Project documentation
├── requirements.txt              # Python package dependencies
└── .gitignore                    # Git exclusions
```

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Install required packages:

```bash
pip install -r requirements.txt
```

---

### Usage

1. Ensure your patient records are saved in `data/patients.csv`.
2. Execute the data cleaner:

```bash
python src/data_cleaner.py
```

3. Outputs:
   - `data/cleaned_patients.csv` — Cleaned dataset
   - `logs/data_cleaning_log.txt` — Validation logs

---

## Input File Format

The input file (`patients.csv`) must contain the following headers:

```csv
patient_id,full_name,date_of_birth,age,phone,email,gender,vitals_notes
```

Sample entry:

```csv
P001,John Doe,1985-01-02,39,555-1234,john.doe@email.com,Male,High Blood Pressure
```

---

## Planned Enhancements

- [ ] PDF report generation for each patient
- [ ] Automated email delivery of patient summaries
- [ ] CLI argument parsing for file paths and patient selection
- [ ] Unit testing of core functionality
- [ ] REST API interface via FastAPI

---

## Author

Developed by Rafael Puente — Computer Science student and aspiring network administrator or anything!!!

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software with appropriate attribution.

---

## Contact

For inquiries or collaboration, feel free to reach out via GitHub or LinkedIn.

