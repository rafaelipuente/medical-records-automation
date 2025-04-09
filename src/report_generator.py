import pandas as pd
from fpdf import FPDF
import os
import argparse
from pathlib import Path
import numpy as np

# Set matplotlib to use non-interactive backend to avoid thread issues
import matplotlib
matplotlib.use('Agg')  # Must be set before importing pyplot
import matplotlib.pyplot as plt

def generate_sample_data():
    data = {
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Davis'],
        'age': np.random.randint(25, 85, 5),
        'blood_pressure': [f'{np.random.randint(110, 160)}/{np.random.randint(70, 100)}' for _ in range(5)],
        'heart_rate': np.random.randint(55, 110, 5),
        'temperature': np.round(np.random.uniform(36.0, 38.5, 5), 1),
        'diagnosis': ['Hypertension', 'Diabetes', 'Arthritis', 'Asthma', 'Migraine']
    }
    return pd.DataFrame(data)

def generate_chart(patient, chart_path):
    labels = ['Heart Rate', 'Temperature']
    values = [patient['heart_rate'], patient['temperature']]

    plt.figure(figsize=(4, 2))
    bars = plt.bar(labels, values)
    plt.title('Vitals Overview')
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

def get_doctor_recommendation(bp, hr, temp):
    try:
        systolic = int(bp.split('/')[0])
        if systolic > 140:
            return "Monitor for hypertension."
        elif hr < 60:
            return "Possible bradycardia, further evaluation needed."
        elif temp > 37.5:
            return "Fever detected — consider further testing."
        else:
            return "Vitals within normal range."
    except:
        return "Unable to analyze vitals."

def create_patient_report(patient_data, output_path):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Patient Health Report', ln=True, align='C')
    pdf.ln(10)

    # Get patient name - handle both 'name' and 'full_name' columns
    patient_name = patient_data.get('full_name', patient_data.get('name', 'Unknown'))

    # Section: Patient Info
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Patient Information', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Name: {patient_name}", ln=True)
    pdf.cell(0, 10, f"Age: {patient_data['age']}", ln=True)
    pdf.ln(5)

    # Section: Vitals
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Vitals', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Blood Pressure: {patient_data['blood_pressure']}", ln=True)
    pdf.cell(0, 10, f"Heart Rate: {patient_data['heart_rate']}", ln=True)
    pdf.cell(0, 10, f"Temperature: {patient_data['temperature']}°C", ln=True)
    pdf.ln(5)

    # Add vitals chart
    chart_path = 'charts/temp_chart.png'
    os.makedirs('charts', exist_ok=True)
    generate_chart(patient_data, chart_path)
    pdf.image(chart_path, x=10, y=pdf.get_y(), w=100)
    pdf.ln(45)

    # Section: Diagnosis
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Diagnosis', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, patient_data['diagnosis'])
    pdf.ln(5)

    # Section: Doctor's Recommendation
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Doctor's Recommendation", ln=True)
    pdf.set_font('Arial', '', 12)
    recommendation = get_doctor_recommendation(patient_data['blood_pressure'], patient_data['heart_rate'], patient_data['temperature'])
    pdf.multi_cell(0, 10, recommendation)

    # Save PDF
    pdf.output(str(output_path))

def main(generate_samples=True, input_file='data/patients.csv', output_folder='patient_reports'):
    try:
        if generate_samples:
            df = generate_sample_data()
            data_path = Path(input_file)
            df.to_csv(data_path, index=False)
            print(f'Sample data saved to {data_path}')
        else:
            df = pd.read_csv(input_file)
            print(f'Read {len(df)} patient records from {input_file}')

        output_folder = Path(output_folder)
        output_folder.mkdir(exist_ok=True)

        for _, patient in df.iterrows():
            # Get patient name - handle both 'name' and 'full_name' columns
            patient_dict = patient.to_dict()
            patient_name = patient_dict.get('full_name', patient_dict.get('name', f'patient_{_}'))
            
            # Create sanitized filename
            filename = f"patient_{str(patient_name).lower().replace(' ', '_')}_report.pdf"
            output_path = output_folder / filename
            
            # Generate the report
            create_patient_report(patient_dict, output_path)
            print(f'Generated report: {output_path}')

        print(f'\nSuccessfully generated {len(df)} patient reports in {output_folder}/')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate patient health reports')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate sample patient data')
    parser.add_argument('-i', '--input', default='data/patients.csv', help='Input CSV file with patient data')
    parser.add_argument('-o', '--output', default='patient_reports', help='Output folder for PDF reports')
    args = parser.parse_args()
    
    main(generate_samples=args.generate, input_file=args.input, output_folder=args.output)
