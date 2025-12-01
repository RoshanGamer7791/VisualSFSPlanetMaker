import customtkinter as ctk

class OrbitEditor:
    def __init__(self, parent, planet_data):
        self.parent = parent
        self.planet_data = planet_data

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        self.vars = {}
        self.build_ui()

    # Helper to create a label + entry pair
    def add_field(self, label, key, default, row):
        ctk.CTkLabel(self.frame, text=label).grid(
            row=row, column=0, padx=10, pady=6, sticky="w"
        )
        var = ctk.StringVar(value=str(default))
        entry = ctk.CTkEntry(self.frame, textvariable=var, width=200)
        entry.grid(row=row, column=1, padx=10, pady=6, sticky="w")
        self.vars[key] = var

    def build_ui(self):
        orbit = self.planet_data.get("ORBIT_DATA", {})

        self.add_field("Parent Body", "parent", orbit.get("parent", "Sun"), 0)
        self.add_field("Semi-Major Axis", "semiMajorAxis", orbit.get("semiMajorAxis", 0), 1)
        self.add_field("Eccentricity", "eccentricity", orbit.get("eccentricity", 0), 2)
        self.add_field("Argument of Periapsis", "argumentOfPeriapsis",
                       orbit.get("argumentOfPeriapsis", 0), 3)
        self.add_field("Direction (1=prograde, -1=retrograde)", "direction",
                       orbit.get("direction", 1), 4)
        self.add_field("Inclination", "inclination", orbit.get("inclination", 0), 5)

    def save(self):
        orbit = self.planet_data.setdefault("ORBIT_DATA", {})

        orbit["parent"] = self.vars["parent"].get()
        orbit["semiMajorAxis"] = float(self.vars["semiMajorAxis"].get() or 0)
        orbit["eccentricity"] = float(self.vars["eccentricity"].get() or 0)
        orbit["argumentOfPeriapsis"] = float(self.vars["argumentOfPeriapsis"].get() or 0)
        orbit["direction"] = int(self.vars["direction"].get() or 1)
        orbit["inclination"] = float(self.vars["inclination"].get() or 0)

    def get_data(self):
        return {
            "ORBIT_DATA": {
                "parent": self.vars["parent"].get(),
                "semiMajorAxis": float(self.vars["semiMajorAxis"].get() or 0),
                "eccentricity": float(self.vars["eccentricity"].get() or 0),
                "argumentOfPeriapsis": float(self.vars["argumentOfPeriapsis"].get() or 0),
                "direction": int(self.vars["direction"].get() or 1),
                "inclination": float(self.vars["inclination"].get() or 0),
            }
        }
