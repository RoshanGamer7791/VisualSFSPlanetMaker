# gui/planet_properties.py
import tkinter as tk
from tkinter import colorchooser, messagebox

class PlanetPropertiesEditor(tk.Frame):
    def __init__(self, master, planet_data):
        super().__init__(master)
        self.master = master
        self.planet_data = planet_data
        if "BASE_DATA" not in self.planet_data:
            self.planet_data["BASE_DATA"] = {}
        self.create_widgets()

    def create_widgets(self):
        base = self.planet_data["BASE_DATA"]

        # Radius
        tk.Label(self, text="Radius:").grid(row=0, column=0, sticky="e")
        self.entry_radius = tk.Entry(self)
        self.entry_radius.insert(0, str(base.get("radius", 0)))
        self.entry_radius.grid(row=0, column=1)

        # Gravity
        tk.Label(self, text="Gravity:").grid(row=1, column=0, sticky="e")
        self.entry_gravity = tk.Entry(self)
        self.entry_gravity.insert(0, str(base.get("gravity", 0)))
        self.entry_gravity.grid(row=1, column=1)

        # Map Color
        tk.Label(self, text="Map Color (RGBA 0-1):").grid(row=2, column=0, sticky="e")
        self.color_button = tk.Button(self, text="Pick Color", command=self.pick_color)
        self.color_button.grid(row=2, column=1)

        # Difficulty scales
        tk.Label(self, text="Radius Difficulty:").grid(row=3, column=0, sticky="e")
        self.entry_radius_diff = tk.Entry(self)
        self.entry_radius_diff.insert(0, str(base.get("radiusDifficultyScale", {})))
        self.entry_radius_diff.grid(row=3, column=1)

        tk.Label(self, text="Gravity Difficulty:").grid(row=4, column=0, sticky="e")
        self.entry_gravity_diff = tk.Entry(self)
        self.entry_gravity_diff.insert(0, str(base.get("gravityDifficultyScale", {})))
        self.entry_gravity_diff.grid(row=4, column=1)

        # Other base fields
        tk.Label(self, text="Timewarp Height:").grid(row=5, column=0, sticky="e")
        self.entry_timewarp = tk.Entry(self)
        self.entry_timewarp.insert(0, str(base.get("timewarpHeight", 0)))
        self.entry_timewarp.grid(row=5, column=1)

        tk.Label(self, text="Velocity Arrows Height:").grid(row=6, column=0, sticky="e")
        self.entry_velocity = tk.Entry(self)
        self.entry_velocity.insert(0, str(base.get("velocityArrowsHeight", 0)))
        self.entry_velocity.grid(row=6, column=1)

        # Booleans
        self.significant_var = tk.BooleanVar(value=base.get("significant", True))
        tk.Checkbutton(self, text="Significant", variable=self.significant_var).grid(row=7, column=0, columnspan=2)

        self.rotate_var = tk.BooleanVar(value=base.get("rotateCamera", True))
        tk.Checkbutton(self, text="Rotate Camera", variable=self.rotate_var).grid(row=8, column=0, columnspan=2)

    def pick_color(self):
        color = colorchooser.askcolor()[0]  # returns (r,g,b)
        if color:
            r, g, b = color
            self.planet_data["BASE_DATA"]["mapColor"] = {
                "r": r / 255,
                "g": g / 255,
                "b": b / 255,
                "a": 1.0
            }

    def update_planet_data(self):
        base = self.planet_data["BASE_DATA"]
        try:
            base["radius"] = float(self.entry_radius.get())
            base["gravity"] = float(self.entry_gravity.get())
            base["timewarpHeight"] = float(self.entry_timewarp.get())
            base["velocityArrowsHeight"] = float(self.entry_velocity.get())

            # Keep difficulty scales as dictionaries
            base["radiusDifficultyScale"] = eval(self.entry_radius_diff.get())
            base["gravityDifficultyScale"] = eval(self.entry_gravity_diff.get())

            base["significant"] = self.significant_var.get()
            base["rotateCamera"] = self.rotate_var.get()

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
