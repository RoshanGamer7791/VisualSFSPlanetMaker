# gui/orbit_editor.py
import tkinter as tk
from tkinter import ttk, messagebox

class OrbitEditor(tk.Frame):
    def __init__(self, master, planet_data):
        super().__init__(master)
        self.master = master
        self.planet_data = planet_data
        if "ORBIT_DATA" not in self.planet_data:
            self.planet_data["ORBIT_DATA"] = {}
        self.create_widgets()

    def create_widgets(self):
        orbit = self.planet_data["ORBIT_DATA"]

        # Parent Body
        tk.Label(self, text="Parent Body:").grid(row=0, column=0, sticky="e")
        self.entry_parent = tk.Entry(self)
        self.entry_parent.insert(0, orbit.get("parent", "Sun"))
        self.entry_parent.grid(row=0, column=1)

        # Semi-major Axis
        tk.Label(self, text="Semi-Major Axis (m):").grid(row=1, column=0, sticky="e")
        self.entry_sma = tk.Entry(self)
        self.entry_sma.insert(0, str(orbit.get("semiMajorAxis", 0.0)))
        self.entry_sma.grid(row=1, column=1)

        # Eccentricity
        tk.Label(self, text="Eccentricity:").grid(row=2, column=0, sticky="e")
        self.entry_ecc = tk.Entry(self)
        self.entry_ecc.insert(0, str(orbit.get("eccentricity", 0.0)))
        self.entry_ecc.grid(row=2, column=1)

        # Argument of Periapsis
        tk.Label(self, text="Argument of Periapsis:").grid(row=3, column=0, sticky="e")
        self.entry_arg = tk.Entry(self)
        self.entry_arg.insert(0, str(orbit.get("argumentOfPeriapsis", 0.0)))
        self.entry_arg.grid(row=3, column=1)

        # Direction
        tk.Label(self, text="Direction (1 = prograde, -1 = retrograde):").grid(row=4, column=0, sticky="e")
        self.entry_dir = tk.Entry(self)
        self.entry_dir.insert(0, str(orbit.get("direction", 1)))
        self.entry_dir.grid(row=4, column=1)

        # Multiplier SOI
        tk.Label(self, text="SOI Multiplier:").grid(row=5, column=0, sticky="e")
        self.entry_soi = tk.Entry(self)
        self.entry_soi.insert(0, str(orbit.get("multiplierSOI", 2.5)))
        self.entry_soi.grid(row=5, column=1)

        # Difficulty Scales
        scales = ["smaDifficultyScale", "soiDifficultyScale"]
        for i, scale_name in enumerate(scales):
            tk.Label(self, text=f"{scale_name} (Normal, Hard, Realistic, comma-separated):").grid(row=6+i, column=0, sticky="e")
            scale_dict = orbit.get(scale_name, {})
            normal = scale_dict.get("Normal", 1.0)
            hard = scale_dict.get("Hard", 1.0)
            realistic = scale_dict.get("Realistic", 1.0)
            entry = tk.Entry(self)
            entry.insert(0, f"{normal},{hard},{realistic}")
            entry.grid(row=6+i, column=1)
            setattr(self, f"entry_{scale_name}", entry)

        # Preview Placeholder
        tk.Label(self, text="Orbit Preview:").grid(row=8, column=0, sticky="ne")
        self.preview_canvas = tk.Canvas(self, width=300, height=200, bg="black")
        self.preview_canvas.grid(row=8, column=1)
        self.preview_canvas.create_text(150, 100, fill="white", text="Preview system placeholder")

    def update_planet_data(self):
        orbit = self.planet_data["ORBIT_DATA"]
        orbit["parent"] = self.entry_parent.get()
        orbit["semiMajorAxis"] = float(self.entry_sma.get())
        orbit["eccentricity"] = float(self.entry_ecc.get())
        orbit["argumentOfPeriapsis"] = float(self.entry_arg.get())
        orbit["direction"] = int(self.entry_dir.get())
        orbit["multiplierSOI"] = float(self.entry_soi.get())

        # Update difficulty scales
        for scale_name in ["smaDifficultyScale", "soiDifficultyScale"]:
            entry_text = getattr(self, f"entry_{scale_name}").get()
            values = entry_text.split(",")
            orbit[scale_name] = {
                "Normal": float(values[0]) if len(values) > 0 else 1.0,
                "Hard": float(values[1]) if len(values) > 1 else 1.0,
                "Realistic": float(values[2]) if len(values) > 2 else 1.0
            }
