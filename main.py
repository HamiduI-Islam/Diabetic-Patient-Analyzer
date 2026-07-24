import tkinter as tk
from tkinter import ttk, messagebox
from model import Patient
from file_manager import DataManager
from analytics import HealthAnalytics

class AdminDashboard:
    """
    Tkinter application class focused on the administrative user role.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("System Administration - Diabetic Patient Analyzer")
        self.root.geometry("800x650")
        
        #light blue background to the main window
        self.root.configure(bg="#f0f8ff", padx=20, pady=20)
        
        #  modern theme with custom light blue/white colors
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        # Configure global ttk styles
        style.configure(".", background="#f0f8ff") 
        style.configure("TLabelframe", background="#ffffff") 
        style.configure("TLabelframe.Label", background="#f0f8ff", foreground="#00509e", font=("Helvetica", 10, "bold"))
        style.configure("TLabel", background="#ffffff") 
        
        # Configure Buttons with a soft blue tint and darker hover effect
        style.configure("TButton", background="#e6f2ff", borderwidth=1)
        style.map("TButton", background=[("active", "#cce6ff")])

        # Initialize the backend DataManager
        self.data_manager = DataManager()
        self.patient_db, self.active_ids = self.data_manager.load_records()

        self.setup_ui()
        self.refresh_listbox()

    def setup_ui(self):
        """Sets up the administrative interface components."""
        
       # --- HEADER ---
        header = tk.Label(
            self.root, 
            text="CLINICAL DATA MANAGEMENT", 
            font=("Helvetica", 16, "bold"), 
            bg="#f0f8ff",  # Matches the main window background
            fg="#2578ca"   # Dark blue text for contrast
        )
        header.pack(pady=(0, 15))
       

        # --- TOP PANEL: Administrative Data Entry ---
        input_frame = ttk.LabelFrame(self.root, text=" Data Entry Form ", padding=(255, 10))
        input_frame.pack(fill=tk.X, pady=5)

        fields = ['Patient ID', 'Age', 'Glucose', 'Blood Pressure', 'BMI', 'Insulin', 'Outcome (1=Yes, 0=No)']
        self.entries = {}
        
        # Use a 2-column grid layout 
        for i, field in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2
            ttk.Label(input_frame, text=field + ":", font=("Helvetica", 10)).grid(row=row, column=col, sticky='e', padx=10, pady=8)
            entry = ttk.Entry(input_frame, width=22)
            entry.grid(row=row, column=col+1, padx=10, pady=8)
            self.entries[field] = entry

        # --- MIDDLE PANEL: System Actions ---
        button_frame = ttk.LabelFrame(self.root, text=" System Actions ", padding=(15, 10))
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="➕ Add Record", command=self.add_record).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="🔍 Search By ID", command=self.search_record).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="✏️ Update Info", command=self.update_record).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="❌ Delete By ID", command=self.delete_record).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="📊 View Stats", command=self.view_statistics).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="💾 Save Database", command=self.save_data).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # --- BOTTOM PANEL: Active Database View ---
        list_frame = ttk.LabelFrame(self.root, text=" Active Records ", padding=(15, 10))
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)


       # Enhanced listbox with custom fonts and light blue selection colors
        self.listbox = tk.Listbox(
            list_frame, 
            width=80, 
            height=10, 
            font=("Consolas", 11), 
            bg="#ffffff",               # White background
            fg="#333333",               # Dark gray text
            selectbackground="#77b5ef", # Light blue when an item is clicked
            selectforeground="black",   # Black text when selected
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor="#a1c8ed"
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

    def refresh_listbox(self):
        """Clears and repopulates the listbox with the current administrative database."""
        self.listbox.delete(0, tk.END)
        for p_id in sorted(self.patient_db.keys()):
            self.listbox.insert(tk.END, str(self.patient_db[p_id]))

    def clear_entries(self):
        """Clears the input fields after successful entry."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def add_record(self):
        """Validates input and adds a new patient to the database."""
        try:
            p_id = int(self.entries['Patient ID'].get())
            if p_id in self.active_ids:
                messagebox.showerror("Compliance Error", f"ID {p_id} already exists in the system.")
                return

            age = int(self.entries['Age'].get())
            if age < 0:
                messagebox.showerror("Validation Error", "Age cannot be negative.")
                return

            new_patient = Patient(
                patient_id=p_id,
                age=age,
                glucose=self.entries['Glucose'].get(),
                blood_pressure=self.entries['Blood Pressure'].get(),
                bmi=self.entries['BMI'].get(),
                insulin=self.entries['Insulin'].get(),
                outcome=self.entries['Outcome (1=Yes, 0=No)'].get()
            )
            
            self.patient_db[p_id] = new_patient
            self.active_ids.add(p_id)
            self.refresh_listbox()
            self.clear_entries()
            messagebox.showinfo("Success", f"Patient ID {p_id} successfully added.")
            
        except ValueError:
            messagebox.showerror("Data Error", "Please ensure all required fields contain valid numeric data.")

    def update_record(self):
        """Validates input, updates an existing patient record, and auto-saves to the file."""
        try:
            p_id = int(self.entries['Patient ID'].get())
            
            # Admin Validation: Ensure the ID exists before allowing an overwrite
            if p_id not in self.active_ids:
                messagebox.showerror("Compliance Error", f"ID {p_id} does not exist in the system. Cannot update.")
                return

            age = int(self.entries['Age'].get())
            if age < 0:
                messagebox.showerror("Validation Error", "Age cannot be negative.")
                return

            # Overwrite the existing record with the modified data from the UI
            updated_patient = Patient(
                patient_id=p_id,
                age=age,
                glucose=self.entries['Glucose'].get(),
                blood_pressure=self.entries['Blood Pressure'].get(),
                bmi=self.entries['BMI'].get(),
                insulin=self.entries['Insulin'].get(),
                outcome=self.entries['Outcome (1=Yes, 0=No)'].get()
            )
            
            # Update the dictionary and refresh UI
            self.patient_db[p_id] = updated_patient
            self.refresh_listbox()
            self.clear_entries()
            
            # Save the updated database directly to the file
            self.data_manager.save_records(self.patient_db)
            
            messagebox.showinfo("Update Successful", f"Patient ID {p_id} updated and saved to the database.")
            
        except ValueError:
            messagebox.showerror("Data Error", "Please ensure all required fields contain valid numeric data.")
    def search_record(self):
        """Looks up a specific ID and populates the entry fields for viewing or updating."""
        try:
            # We only need the ID to search, so we extract it first
            search_id_text = self.entries['Patient ID'].get()
            if not search_id_text:
                messagebox.showerror("Input Error", "Please enter a Patient ID to search.")
                return
                
            search_id = int(search_id_text)
            
            if search_id in self.patient_db:
                patient = self.patient_db[search_id]
                
                # Clear the form completely before inserting the found data
                self.clear_entries()
                
                # Populate the fields with the patient's existing records
                self.entries['Patient ID'].insert(0, str(patient.patient_id))
                self.entries['Age'].insert(0, str(patient.age))
                self.entries['Glucose'].insert(0, str(patient.glucose))
                self.entries['Blood Pressure'].insert(0, str(patient.blood_pressure))
                self.entries['BMI'].insert(0, str(patient.bmi))
                self.entries['Insulin'].insert(0, str(patient.insulin))
                self.entries['Outcome (1=Yes, 0=No)'].insert(0, str(patient.outcome))
                
                
                messagebox.showinfo("Record Found", f"Patient ID {search_id} loaded into the form for review or editing.")
            else:
                messagebox.showwarning("Not Found", f"Patient ID {search_id} does not exist.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric ID to search.")

    def delete_record(self):
        """Removes a patient record from the active session."""
        try:
            delete_id = int(self.entries['Patient ID'].get())
            if delete_id in self.patient_db:
                del self.patient_db[delete_id]
                self.active_ids.remove(delete_id)
                self.refresh_listbox()
                self.clear_entries()
                messagebox.showinfo("Success", f"Patient ID {delete_id} has been removed.")
            else:
                messagebox.showwarning("Not Found", f"Patient ID {delete_id} does not exist.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric ID to delete.")

    def view_statistics(self):
        """Triggers the NumPy analytics and displays the administrative summary."""
        stats_tuple = HealthAnalytics.generate_clinical_summary(self.patient_db)
        formatted_stats = "\n\n".join(stats_tuple)
        messagebox.showinfo("Clinical Diagnostics Summary", formatted_stats)

    def save_data(self):
        """Saves current memory to the CSV file."""
        self.data_manager.save_records(self.patient_db)
        messagebox.showinfo("System Update", "All records have been securely saved to the database.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()