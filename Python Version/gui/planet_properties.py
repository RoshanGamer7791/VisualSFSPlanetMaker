import customtkinter as ctk

class PlanetPropertiesEditor:
    def __init__(self, parent, planet_data):
        self.parent = parent
        self.planet_data = planet_data
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        base = self.planet_data.get("BASE_DATA", {})

        # Radius
        self.radius_var = ctk.StringVar(value=str(base.get("radius", 0)))
        ctk.CTkLabel(self.frame, text="Radius").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.radius_var).grid(row=0, column=1, padx=5, pady=5)

        # Gravity
        self.gravity_var = ctk.StringVar(value=str(base.get("gravity", 0)))
        ctk.CTkLabel(self.frame, text="Gravity").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.gravity_var).grid(row=1, column=1, padx=5, pady=5)

        # Timewarp Height
        self.timewarp_var = ctk.StringVar(value=str(base.get("timewarpHeight", 0)))
        ctk.CTkLabel(self.frame, text="Timewarp Height").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.timewarp_var).grid(row=2, column=1, padx=5, pady=5)

        # Velocity Arrows Height
        self.velar_var = ctk.StringVar(value=str(base.get("velocityArrowsHeight", 0)))
        ctk.CTkLabel(self.frame, text="Velocity Arrows Height").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.velar_var).grid(row=3, column=1, padx=5, pady=5)

        # Map Color
        map_color = base.get("mapColor", {})
        self.map_r_var = ctk.StringVar(value=str(map_color.get("r", 0)))
        self.map_g_var = ctk.StringVar(value=str(map_color.get("g", 0)))
        self.map_b_var = ctk.StringVar(value=str(map_color.get("b", 0)))
        self.map_a_var = ctk.StringVar(value=str(map_color.get("a", 1)))

        ctk.CTkLabel(self.frame, text="Map Color R").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.map_r_var).grid(row=4, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Map Color G").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.map_g_var).grid(row=5, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Map Color B").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.map_b_var).grid(row=6, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Map Color A").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.map_a_var).grid(row=7, column=1, padx=5, pady=5)

        # Significant
        self.significant_var = ctk.StringVar(value=str(base.get("significant", True)))
        ctk.CTkLabel(self.frame, text="Significant").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.significant_var).grid(row=8, column=1, padx=5, pady=5)

        # Rotate Camera
        self.rotate_var = ctk.StringVar(value=str(base.get("rotateCamera", True)))
        ctk.CTkLabel(self.frame, text="Rotate Camera").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.frame, textvariable=self.rotate_var).grid(row=9, column=1, padx=5, pady=5)

    def save(self):
        # Push changes back into planet_data
        base = self.planet_data.setdefault("BASE_DATA", {})
        base["radius"] = float(self.radius_var.get())
        base["gravity"] = float(self.gravity_var.get())
        base["timewarpHeight"] = float(self.timewarp_var.get())
        base["velocityArrowsHeight"] = float(self.velar_var.get())
        base["mapColor"] = {
            "r": float(self.map_r_var.get()),
            "g": float(self.map_g_var.get()),
            "b": float(self.map_b_var.get()),
            "a": float(self.map_a_var.get())
        }
        # For JSON-style boolean fields, keep lowercase true/false as SFS expects
        base["significant"] = True if self.significant_var.get().lower() in ["true", "1"] else False
        base["rotateCamera"] = True if self.rotate_var.get().lower() in ["true", "1"] else False

    def get_data(self):
        return {
            "BASE_DATA": {
                "radius": float(self.radius_var.get() or 0),
                "gravity": float(self.gravity_var.get() or 0),
                "timewarpHeight": float(self.timewarp_var.get() or 25000),
                "velocityArrowsHeight": float(self.velar_var.get() or 5000),
                "mapColor": {
                    "r": float(self.map_r_var.get() or 0),
                    "g": float(self.map_g_var.get() or 0),
                    "b": float(self.map_b_var.get() or 0),
                    "a": float(self.map_a_var.get() or 1)
                },
                "significant": True if self.significant_var.get().lower() in ["true", "1"] else False,
                "rotateCamera": True if self.rotate_var.get().lower() in ["true", "1"] else False
            }
        }

   
