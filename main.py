import tkinter as tk
from tkinter import ttk, messagebox
from model import Patient
from file_manager import DataManager
from analytics import HealthAnalytics

class AdminDashboard:
    """
    The main Tkinter application class focused on the administrative user role.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("System Administration - Diabetic Patient Analyzer")
        self.root.geometry("800x650")
        self.root.configure(padx=20, pady=20)
        
        # Apply a clean, modern theme to the entire application
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

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
            fg="#2c3e50"
        )
        header.pack(pady=(0, 15))

        # --- TOP PANEL: Administrative Data Entry ---
        input_frame = ttk.LabelFrame(self.root, text=" Data Entry Form ", padding=(15, 10))
        input_frame.pack(fill=tk.X, pady=5)

        fields = ['Patient ID', 'Age', 'Glucose', 'Blood Pressure', 'BMI', 'Insulin', 'Outcome (1=Yes, 0=No)']
        self.entries = {}
        
        # Use a 2-column grid layout for a compact, professional form
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

        # Expanding buttons to fill the row evenly
        ttk.Button(button_frame, text="➕ Add Record", command=self.add_record).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="🔍 Search ID", command=self.search_record).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="❌ Delete ID", command=self.delete_record).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="📊 View Stats", command=self.view_statistics).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="💾 Save Database", command=self.save_data).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # --- BOTTOM PANEL: Active Database View ---
        list_frame = ttk.LabelFrame(self.root, text=" Active Records ", padding=(15, 10))
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)


        #
        # Enhanced listbox with custom fonts and selection colors
        self.listbox = tk.Listbox(
            list_frame, 
            width=80, 
            height=10, 
            font=("Consolas", 11), 
            bg="#f8f9fa", 
            selectbackground="#2c3e50",
            selectforeground="white"
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

    def search_record(self):
        """Looks up a specific ID in the dictionary."""
        try:
            search_id = int(self.entries['Patient ID'].get())
            if search_id in self.patient_db:
                patient = self.patient_db[search_id]
                messagebox.showinfo("Record Found", str(patient))
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