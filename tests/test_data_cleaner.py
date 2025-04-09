import unittest
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_cleaner import clean_name, clean_phone, clean_csv

class TestDataCleaner(unittest.TestCase):
    
    def test_clean_phone(self):
        self.assertEqual('"5551234567"', clean_phone('555-123-4567'))
        self.assertEqual('"5551234567"', clean_phone('(555) 123-4567'))
        self.assertEqual('"5551234567"', clean_phone('555.123.4567'))
        self.assertEqual('', clean_phone(''))
        self.assertEqual('', clean_phone(None))
    
    def test_clean_name(self):
        self.assertEqual('John Doe', clean_name('john DOE'))
        self.assertEqual('Jane Smith', clean_name('JANE smith'))
        self.assertEqual('', clean_name(''))
        self.assertEqual('', clean_name(None))
    
    def test_clean_csv_functionality(self):
        # Create a temporary test file
        test_dir = Path('test_data')
        test_dir.mkdir(exist_ok=True)
        
        test_input = test_dir / 'test_input.csv'
        test_output = test_dir / 'test_output.csv'
        test_log = test_dir / 'test_log.txt'
        
        # Write test data
        with open(test_input, 'w') as f:
            f.write('patient_id,full_name,date_of_birth,age,phone,vitals_notes\n')
            f.write('P001,john DOE,1980-01-15,43,555-123-4567,"BP: 120/80, HR: 72"\n')
            f.write('P002,JANE smith,1975-05-20,48,(555) 987-6543,"BP: 130/85, HR: 75"\n')
        
        # Run the clean_csv function
        result = clean_csv(test_input, test_output, test_log)
        
        # Verify result
        self.assertTrue(result)
        self.assertTrue(test_output.exists())
        
        # Cleanup
        test_input.unlink(missing_ok=True)
        test_output.unlink(missing_ok=True)
        test_log.unlink(missing_ok=True)
        test_dir.rmdir()

if __name__ == '__main__':
    unittest.main()
