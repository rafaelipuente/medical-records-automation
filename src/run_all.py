#!/usr/bin/env python3
import argparse
import subprocess
import os
from pathlib import Path

def run_step(command, description):
    """Run a command step and display its description"""
    print(f"\n{'=' * 60}")
    print(f"STEP: {description}")
    print(f"COMMAND: {' '.join(command)}")
    print('=' * 60)

    result = subprocess.run(command, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(f"ERRORS:\n{result.stderr}")
    
    return result.returncode == 0

def run_automation(args):
    """Run the complete patient data automation pipeline"""
    success = True
    steps_completed = 0
    
    # Step 1: Clean the data
    if args.clean:
        clean_cmd = ['python3', 'src/data_cleaner.py', 
                     '-i', args.input, 
                     '-o', args.cleaned_output, 
                     '-l', args.log]
        if not run_step(clean_cmd, "Cleaning patient data"):
            print("❌ Data cleaning failed, stopping pipeline")
            return False
        steps_completed += 1

    # Step 2: Generate reports
    if args.reports:
        reports_cmd = ['python3', 'src/report_generator.py']
        if args.generate_samples:
            reports_cmd.append('--generate')
        else:
            reports_cmd.extend(['-i', args.cleaned_output])
        reports_cmd.extend(['-o', args.report_folder])
        
        if not run_step(reports_cmd, "Generating patient reports"):
            print("❌ Report generation failed, stopping pipeline")
            return False
        steps_completed += 1

    # Step 3: Send emails with reports
    if args.email:
        email_cmd = ['python3', 'src/email_sender.py', 
                     '-c', args.cleaned_output, 
                     '-r', args.report_folder]
        
        if args.email_address:
            email_cmd.extend(['-e', args.email_address])
        if args.email_password:
            email_cmd.extend(['-p', args.email_password])
        
        # Use demo mode by default unless explicitly set to send
        if not args.send:
            email_cmd.append('--demo')
        
        if not run_step(email_cmd, "Processing emails" + (" (DEMO MODE)" if not args.send else "")):
            print("❌ Email processing failed")
            success = False
        steps_completed += 1

    # Step 4: Run tests if requested
    if args.test:
        test_cmd = ['python3', '-m', 'unittest', 'discover', 'tests']
        run_step(test_cmd, "Running tests")
        steps_completed += 1

    print(f"\n{'=' * 60}")
    if success:
        print(f"✅ Automation completed successfully! ({steps_completed} steps)")
    else:
        print(f"⚠️ Automation completed with some issues ({steps_completed} steps)")
    print('=' * 60)
    
    return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patient Data Automation Pipeline")
    
    # Pipeline configuration
    parser.add_argument('--all', action='store_true', help='Run all steps (clean, reports, email)')
    parser.add_argument('--clean', action='store_true', help='Clean the patient data')
    parser.add_argument('--reports', action='store_true', help='Generate patient reports')
    parser.add_argument('--email', action='store_true', help='Process emails (demo mode by default)')
    parser.add_argument('--test', action='store_true', help='Run tests after processing')
    
    # Data options
    parser.add_argument('-i', '--input', default='data/patients.csv', help='Path to input CSV file')
    parser.add_argument('-o', '--cleaned-output', default='data/cleaned_patients.csv', help='Path to cleaned output CSV')
    parser.add_argument('-l', '--log', default='logs/data_cleaning_log.txt', help='Path to log file')
    parser.add_argument('-r', '--report-folder', default='patient_reports', help='Folder for PDF reports')
    parser.add_argument('-g', '--generate-samples', action='store_true', help='Generate sample patient data')
    
    # Email options
    parser.add_argument('-e', '--email-address', help='Email address for sending reports')
    parser.add_argument('-p', '--email-password', help='Email application password')
    parser.add_argument('-s', '--send', action='store_true', help='Actually send emails (not demo mode)')

    args = parser.parse_args()
    
    # If --all flag is specified, enable all processing steps
    if args.all:
        args.clean = True
        args.reports = True
        args.email = True
    
    # If no steps specified, show help
    if not (args.clean or args.reports or args.email or args.test):
        parser.print_help()
        exit(1)
    
    # Ensure required directories exist
    Path('logs').mkdir(exist_ok=True)
    Path('data').mkdir(exist_ok=True)
    Path(args.report_folder).mkdir(exist_ok=True)
    
    # Run the automation
    run_automation(args)
