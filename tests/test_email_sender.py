import unittest
import sys
import os
import tempfile
from pathlib import Path

# Add parent directory to path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.email_sender import generate_email, clean_name, read_csv_manually

class TestEmailSender(unittest.TestCase):
    
    def test_generate_email(self):
        self.assertEqual('john.doe@example.com', generate_email('John Doe'))
        self.assertEqual('jane.smith@example.com', generate_email('Jane Smith'))
        self.assertEqual('alice.johnson@example.com', generate_email('Alice Johnson'))
    
    def test_clean_name(self):
        self.assertEqual('John Doe', clean_name('john DOE'))
        self.assertEqual('Jane Smith', clean_name('JANE smith'))
        self.assertEqual('', clean_name(''))
        self.assertEqual('', clean_name(None))
    
    def test_read_csv_manually(self):
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp:
            temp.write('patient_id,full_name,date_of_birth,age,phone,vitals_notes\n')
            temp.write('P001,John Doe,1980-01-15,43,555-123-4567,"BP: 120/80, HR: 72"\n')
            temp.write('P002,Jane Smith,1975-05-20,48,555-987-6543,"BP: 130/85, HR: 75, TEMP: 36.8"\n')
            temp_path = temp.name
        
        try:
            # Read the CSV manually
            df = read_csv_manually(temp_path)
            
            # Verify results
            self.assertEqual(2, len(df))
            self.assertEqual('John Doe', df.iloc[0]['full_name'])
            self.assertEqual('Jane Smith', df.iloc[1]['full_name'])
            self.assertEqual('BP: 130/85, HR: 75, TEMP: 36.8', df.iloc[1]['vitals_notes'])
        finally:
            # Cleanup
            os.unlink(temp_path)

if __name__ == '__main__':
    unittest.main()
