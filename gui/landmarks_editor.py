# gui/landmarks_editor.py
import tkinter as tk
from tkinter import messagebox, simpledialog

class LandmarksEditor(tk.Frame):
    def __init__(self, master, planet_data):
        super().__init__(master)
        self.master = master
        self.planet_data = planet_data
        if "LANDMARKS" not in self.planet_data:
            self.planet_data["LANDMARKS"] = []

        self.create_widgets()
        self.refresh_listbox()

    def create_widgets(self):
        # Listbox of landmarks
        self.listbox = tk.Listbox(self, width=40)
        self.listbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Buttons
        tk.Button(self, text="Add Landmark", command=self.add_landmark).grid(row=1, column=0, pady=5)
        tk.Button(self, text="Edit Landmark", command=self.edit_landmark).grid(row=1, column=1, pady=5)
        tk.Button(self, text="Delete Landmark", command=self.delete_landmark).grid(row=1, column=2, pady=5)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for lm in self.planet_data["LANDMARKS"]:
            display = f"{lm['name']} (Angle: {lm['angle']}, Start: {lm['startAngle']}, End: {lm['endAngle']})"
            self.listbox.insert(tk.END, display)

    def add_landmark(self):
        name = simpledialog.askstring("Landmark Name", "Enter name of the landmark:")
        if not name:
            return
        angle = simpledialog.askfloat("Angle", "Enter angle of the landmark:")
        start_angle = simpledialog.askfloat("Start Angle", "Enter start angle:")
        end_angle = simpledialog.askfloat("End Angle", "Enter end angle:")
        self.planet_data["LANDMARKS"].append({
            "name": name,
            "angle": angle,
            "startAngle": start_angle,
            "endAngle": end_angle
        })
        self.refresh_listbox()

    def edit_landmark(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Landmark", "Please select a landmark to edit.")
            return
        index = selection[0]
        lm = self.planet_data["LANDMARKS"][index]

        name = simpledialog.askstring("Landmark Name", "Enter name of the landmark:", initialvalue=lm["name"])
        if not name:
            return
        angle = simpledialog.askfloat("Angle", "Enter angle of the landmark:", initialvalue=lm["angle"])
        start_angle = simpledialog.askfloat("Start Angle", "Enter start angle:", initialvalue=lm["startAngle"])
        end_angle = simpledialog.askfloat("End Angle", "Enter end angle:", initialvalue=lm["endAngle"])

        self.planet_data["LANDMARKS"][index] = {
            "name": name,
            "angle": angle,
            "startAngle": start_angle,
            "endAngle": end_angle
        }
        self.refresh_listbox()

    def delete_landmark(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Landmark", "Please select a landmark to delete.")
            return
        index = selection[0]
        del self.planet_data["LANDMARKS"][index]
        self.refresh_listbox()
