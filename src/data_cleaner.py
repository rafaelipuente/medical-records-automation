import pandas as pd
import csv
from pathlib import Path
import re
import argparse
from datetime import datetime

def clean_phone(phone):
    """Clean and standardize phone numbers"""
    if pd.isnull(phone):
        return ''
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', str(phone))
    # Format if we have 10 digits
    return f'"{digits}"' if digits else ''

def clean_name(name):
    """Clean and standardize names"""
    if pd.isnull(name):
        return ''
    # Capitalize each word
    return ' '.join(word.capitalize() for word in str(name).lower().split())

def clean_csv(input_file='data/patients.csv', output_file='data/cleaned_patients.csv', log_file='logs/data_cleaning_log.txt'):
    
    # Ensure log directory exists
    Path('logs').mkdir(exist_ok=True)
    
    with open(log_file, 'w') as log:
        try:
            # Read the raw CSV data as text first
            with open(input_file, 'r') as f:
                lines = f.readlines()
            
            # Process header
            headers = [h.strip() for h in lines[0].strip().split(',')]
            cleaned_lines = [','.join(headers)]
            
            # Process each data line
            for i, line in enumerate(lines[1:], 1):
                try:
                    # Split the line, respecting quoted values
                    row = list(csv.reader([line.strip()]))[0]
                    
                    # Ensure we have the right number of fields
                    while len(row) < len(headers):
                        row.append('')
                    if len(row) > len(headers):
                        # Combine extra fields into the last field
                        row = row[:len(headers)-1] + [' '.join(row[len(headers)-1:])]
                    
                    # Clean specific fields
                    row_dict = dict(zip(headers, row))
                    
                    # Clean full name
                    if 'full_name' in row_dict:
                        row_dict['full_name'] = clean_name(row_dict['full_name'])
                    
                    # Clean phone
                    if 'phone' in row_dict:
                        row_dict['phone'] = clean_phone(row_dict['phone'])
                    
                    # Reconstruct the row in the correct order
                    cleaned_row = [str(row_dict.get(h, '')).strip() for h in headers]
                    
                    # Quote all fields
                    quoted_row = [f'"{field}"' if field and ',' in field else field for field in cleaned_row]
                    
                    cleaned_lines.append(','.join(quoted_row))
                    log.write(f"Processed line {i} successfully\n")
                    
                except Exception as e:
                    log.write(f"Error processing line {i}: {e}\n")
                    # Add empty row to maintain line count
                    cleaned_lines.append(','.join([''] * len(headers)))
            
            # Write the cleaned data
            with open(output_file, 'w') as f:
                f.write('\n'.join(cleaned_lines))
            
            log.write(f"\nCleaned data saved to {output_file}\n")
            
            # Verify the cleaned file
            df = pd.read_csv(output_file)
            log.write(f"Successfully verified the cleaned CSV file.\n")
            log.write(f"Found {len(df)} patient records.\n")
            
        except Exception as e:
            log.write(f"\nError: {e}\n")
            return False
    
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean and standardize patient CSV data')
    parser.add_argument('-i', '--input', default='data/patients.csv', help='Input CSV file path')
    parser.add_argument('-o', '--output', default='data/cleaned_patients.csv', help='Output CSV file path')
    parser.add_argument('-l', '--log', default='logs/data_cleaning_log.txt', help='Log file path')
    args = parser.parse_args()
    
    if clean_csv(args.input, args.output, args.log):
        print(f"Data cleaning completed successfully. Check {args.log} for details.")
    else:
        print(f"Error during data cleaning. Check {args.log} for details.")
