import yagmail
import pandas as pd
from pathlib import Path
import csv
import argparse

def generate_email(name):
    """Generate a simple email from the name (for demo purposes only)"""
    return f"{name.lower().replace(' ', '.')}@example.com"

def clean_name(name):
    """Clean and standardize patient names"""
    if pd.isnull(name) or name is None:
        return ''
    return ' '.join(word.capitalize() for word in str(name).lower().split())

def read_csv_manually(file_path):
    """Read CSV file manually to handle problematic formatting"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Get headers
    headers = [h.strip() for h in lines[0].strip().split(',')]
    data = []
    
    # Process each line
    for line in lines[1:]:
        # Use csv module to handle quoted fields properly
        row = list(csv.reader([line.strip()]))[0]
        
        # Ensure correct number of fields
        while len(row) < len(headers):
            row.append('')
        if len(row) > len(headers):
            # Combine extra fields into the last field
            row = row[:len(headers)-1] + [' '.join(row[len(headers)-1:])]
        
        data.append(dict(zip(headers, row)))
    
    return pd.DataFrame(data)

def send_reports(csv_path='data/patients.csv', report_folder='patient_reports', sender_email="your_email@gmail.com", sender_password="your_app_password", demo_mode=True):

    try:
        # Try different methods to read the CSV
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            print(f"Standard CSV reading failed, trying manual parsing: {e}")
            df = read_csv_manually(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Check for column names and handle both possibilities
    name_column = 'name' if 'name' in df.columns else 'full_name'
    
    # Clean names and generate emails
    df['clean_name'] = df[name_column].apply(clean_name)
    df['email'] = df['clean_name'].apply(generate_email)

    # Create a name-to-email map
    email_map = {name.lower().replace(" ", "_"): email 
                for name, email in zip(df['clean_name'], df['email'])}

    # Set up Yagmail if not in demo mode
    if not demo_mode:
        yag = yagmail.SMTP(user=sender_email, password=sender_password)

    report_folder = Path(report_folder)
    if not report_folder.exists():
        print(f"No reports found in {report_folder}")
        return

    sent_count = 0

    print("\nPatient email mapping:")
    for name, email in email_map.items():
        print(f"{name}: {email}")
    print()

    pdf_files = list(report_folder.glob("*.pdf"))
    if not pdf_files:
        print("No PDF reports found to send")
        return

    for report_file in pdf_files:
        try:
            # Extract patient name slug from filename
            filename_parts = report_file.stem.split("patient_")[1].split("_report")
            name_slug = filename_parts[0]

            if name_slug in email_map:
                recipient = email_map[name_slug]
                subject = "Your Personalized Patient Health Report"
                body = f"Hello,\n\nAttached is your health report.\n\nRegards,\nYour Clinic Team"

                if demo_mode:
                    # For demo purposes, just show what would be sent
                    print(f"✅ Would send: {report_file.name} to {recipient}")
                    sent_count += 1
                else:
                    # Actually send the email
                    print(f"📧 Sending: {report_file.name} to {recipient}")
                    yag.send(to=recipient, subject=subject, contents=body, attachments=str(report_file))
                    sent_count += 1
            else:
                print(f"⚠️ Skipped: No email found for {name_slug}")
        except Exception as e:
            print(f"Error processing {report_file}: {e}")

    print(f"\nFinished processing {sent_count} report(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send patient reports via email')
    parser.add_argument('-c', '--csv', default='data/patients.csv', help='Path to the patient CSV file')
    parser.add_argument('-r', '--reports', default='patient_reports', help='Folder containing PDF reports')
    parser.add_argument('-e', '--email', default='your_email@gmail.com', help='Sender email address')
    parser.add_argument('-p', '--password', default='your_app_password', help='Email app password')
    parser.add_argument('-d', '--demo', action='store_true', help='Run in demo mode (no emails sent)')
    args = parser.parse_args()
    
    send_reports(
        csv_path=args.csv,
        report_folder=args.reports,
        sender_email=args.email,
        sender_password=args.password,
        demo_mode=args.demo
    )
