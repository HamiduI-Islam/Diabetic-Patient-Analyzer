class Patient:
    """
    Represents a single patient record for administrative management.
    """
    def __init__(self, patient_id, age, glucose, blood_pressure, bmi, insulin, outcome):
        self.patient_id = int(patient_id)
        self.age = int(age)
        
        # Handle potential empty strings from missing dataset records
        self.glucose = int(glucose) if glucose else 0  
        self.blood_pressure = int(blood_pressure) if blood_pressure else 0
        self.bmi = float(bmi) if bmi else 0.0
        self.insulin = int(insulin) if insulin else 0
        
        self.outcome = int(outcome)

    def get_diagnosis_label(self):
        """
        Translates the binary outcome into a readable label for the admin interface.
        """
        if self.outcome == 1:
            return "Diabetic"
        else:
            return "Non-Diabetic"

    def __str__(self):
        """
        Provides a clean, readable string format for the UI listboxes.
        """
        return f"ID: {self.patient_id} | Age: {self.age} | Diagnosis: {self.get_diagnosis_label()}"