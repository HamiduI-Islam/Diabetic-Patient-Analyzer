import numpy as np

class HealthAnalytics:
    """
    Handles statistical analysis of patient records for the administrative dashboard.
    """
    @staticmethod
    def generate_clinical_summary(patient_database):
        """
        Extracts metrics from the patient database and uses NumPy to calculate statistics.
        Returns a tuple of formatted string results.
        """
        if not patient_database:
            return ("No patient records available for analysis.",)

        # 1. Extract data into standard Python lists
        glucose_levels = [p.glucose for p in patient_database.values() if p.glucose > 0]
        blood_pressures = [p.blood_pressure for p in patient_database.values() if p.blood_pressure > 0]
        outcomes = [p.outcome for p in patient_database.values()]

        # 2. Convert lists to NumPy arrays for mathematical analysis
        glucose_arr = np.array(glucose_levels)
        bp_arr = np.array(blood_pressures)
        outcome_arr = np.array(outcomes)

        # 3. Calculate administrative statistics using NumPy functions
        avg_glucose = np.mean(glucose_arr) if glucose_arr.size > 0 else 0.0
        max_bp = np.max(bp_arr) if bp_arr.size > 0 else 0
        
        # 4. Calculate category counts
        total_patients = outcome_arr.size
        diabetic_count = np.sum(outcome_arr == 1)
        diabetic_percentage = (diabetic_count / total_patients) * 100 if total_patients > 0 else 0.0

        # 5. Return the results bundled securely in a Tuple
        return (
            f"Total Active Patients: {total_patients}",
            f"Clinic Average Glucose: {avg_glucose:.1f} mg/dL",
            f"Highest Recorded Blood Pressure: {max_bp} mm Hg",
            f"High-Risk (Diabetic) Population: {diabetic_count} patients ({diabetic_percentage:.1f}%)"
        )