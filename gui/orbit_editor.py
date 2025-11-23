import customtkinter as ctk
import tkinter as tk

class OrbitEditor:
    def __init__(self, parent, planet_data):
        self.parent = parent
        self.planet_data = planet_data
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True)
        self.entries = {}
        self.build_ui()

    def build_ui(self):
        orbit = self.planet_data.get("ORBIT_DATA", {})

        # Parent Star
        self.parent_var = tk.StringVar(value=orbit.get("parent", "Sun"))
        tk.Label(self.frame, text="Parent").grid(row=0, column=0, sticky="w")
        tk.Entry(self.frame, textvariable=self.parent_var).grid(row=0, column=1)

        # Semi-major Axis
        self.sma_var = tk.StringVar(value=str(orbit.get("semiMajorAxis", 0)))
        tk.Label(self.frame, text="Semi-Major Axis").grid(row=1, column=0, sticky="w")
        tk.Entry(self.frame, textvariable=self.sma_var).grid(row=1, column=1)

        # Eccentricity
        self.ecc_var = tk.StringVar(value=str(orbit.get("eccentricity", 0)))
        tk.Label(self.frame, text="Eccentricity").grid(row=2, column=0, sticky="w")
        tk.Entry(self.frame, textvariable=self.ecc_var).grid(row=2, column=1)

        # Argument of Periapsis
        self.argp_var = tk.StringVar(value=str(orbit.get("argumentOfPeriapsis", 0)))
        tk.Label(self.frame, text="Argument of Periapsis").grid(row=3, column=0, sticky="w")
        tk.Entry(self.frame, textvariable=self.argp_var).grid(row=3, column=1)

        # Direction
        self.direction_var = tk.StringVar(value=str(orbit.get("direction", 1)))
        tk.Label(self.frame, text="Direction").grid(row=4, column=0, sticky="w")
        tk.Entry(self.frame, textvariable=self.direction_var).grid(row=4, column=1)


    def save(self):
        orbit = self.planet_data.setdefault("ORBIT_DATA", {})
        orbit["parent"] = self.entries["parent"].get()
        orbit["semiMajorAxis"] = float(self.entries["semiMajorAxis"].get())
        orbit["eccentricity"] = float(self.entries["eccentricity"].get())
        orbit["argumentOfPeriapsis"] = float(self.entries["argumentOfPeriapsis"].get())
        orbit["direction"] = int(self.entries["direction"].get())
        orbit["multiplierSOI"] = float(self.entries["multiplierSOI"].get())

    def get_data(self):
        return {
            "ORBIT_DATA": {
                "parent": self.parent_var.get(),
                "semiMajorAxis": float(self.sma_var.get() or 0),
                "eccentricity": float(self.ecc_var.get() or 0),
                "argumentOfPeriapsis": float(self.argp_var.get() or 0),
                "direction": int(self.direction_var.get() or 1)
            }
        }

