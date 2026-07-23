import csv
import os
from model import Patient

class DataManager:
    """
    Handles secure administrative data ingestion, validation, and file saving.
    """
    def __init__(self, filepath="diabetes_patients.csv"):
        self.filepath = filepath

    def load_records(self):
        """
        Reads the CSV file, validates data, and returns a dictionary of Patient objects.
        """
        patient_database = {}  # Dictionary for fast Admin ID lookups
        active_ids = set()     # Set to strictly audit and prevent duplicate entries

        # Exception Handling: Catch missing file errors gracefully
        if not os.path.exists(self.filepath):
            print(f"Admin Alert: '{self.filepath}' not found. Initializing a new database.")
            return patient_database, active_ids

        with open(self.filepath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    patient_id = int(row['Patient_ID'])
                    
                    # Admin Validation: Reject duplicates
                    if patient_id in active_ids:
                        print(f"Audit Warning: Duplicate Patient ID ({patient_id}) detected and rejected.")
                        continue
                        
                    # Create the Patient model
                    patient = Patient(
                        patient_id=patient_id,
                        age=row['Age'],
                        glucose=row['Glucose'],
                        blood_pressure=row['BloodPressure'],
                        bmi=row['BMI'],
                        insulin=row['Insulin'],
                        outcome=row['Outcome']
                    )
                    
                    patient_database[patient_id] = patient
                    active_ids.add(patient_id)
                    
                # Exception Handling: Catch corrupted data types (like 'NA' strings)
                except ValueError:
                    print("Audit Warning: Corrupted data format found in row. Record skipped.")
                    
        print(f"System Status: Successfully loaded {len(patient_database)} valid administrative records.")
        return patient_database, active_ids

    def save_records(self, patient_database):
        """
        Saves the current session data back to the CSV file to ensure data persistence.
        """
        with open(self.filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write column headers
            writer.writerow(['Patient_ID', 'Age', 'Glucose', 'BloodPressure', 'BMI', 'Insulin', 'Outcome'])
            
            for patient in patient_database.values():
                writer.writerow([
                    patient.patient_id, 
                    patient.age, 
                    patient.glucose, 
                    patient.blood_pressure, 
                    patient.bmi, 
                    patient.insulin, 
                    patient.outcome
                ])
        print("System Status: Administrative database successfully updated and saved.")