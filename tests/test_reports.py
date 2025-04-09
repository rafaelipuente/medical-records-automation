import unittest
from src.report_generator import get_doctor_recommendation, generate_sample_data
import os

class TestPatientReportUtils(unittest.TestCase):

    def test_high_blood_pressure(self):
        rec = get_doctor_recommendation("150/90", 80, 37.0)
        self.assertIn("hypertension", rec.lower())

    def test_low_heart_rate(self):
        rec = get_doctor_recommendation("120/80", 55, 36.8)
        self.assertIn("bradycardia", rec.lower())

    def test_high_temperature(self):
        rec = get_doctor_recommendation("120/80", 70, 38.0)
        self.assertIn("fever", rec.lower())

    def test_normal_vitals(self):
        rec = get_doctor_recommendation("120/80", 72, 36.9)
        self.assertIn("normal", rec.lower())

    def test_generate_sample_data(self):
        df = generate_sample_data()
        self.assertEqual(len(df), 5)
        self.assertIn("name", df.columns)
        self.assertIn("age", df.columns)

if __name__ == '__main__':
    unittest.main()
