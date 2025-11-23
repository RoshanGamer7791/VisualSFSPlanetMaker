import customtkinter as ctk

class AtmosphereEditor:
    def __init__(self, parent, planet_data):
        self.parent = parent
        self.planet_data = planet_data
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True)

        self.entries = {}
        self.build_ui()

    def build_ui(self):
        # Physics Data
        phys = self.planet_data.get("ATMOSPHERE_PHYSICS_DATA", {})
        self.add_label_entry("Height", "height", phys)
        self.add_label_entry("Density", "density", phys)
        self.add_label_entry("Curve", "curve", phys)
        self.add_label_entry("Parachute Multiplier", "parachuteMultiplier", phys)
        self.add_label_entry("Upper Atmosphere", "upperAtmosphere", phys)
        self.add_label_entry("Shockwave Intensity", "shockwaveIntensity", phys)
        self.add_label_entry("Min Heating Velocity Multiplier", "minHeatingVelocityMultiplier", phys)

        # Visuals
        visuals = self.planet_data.get("ATMOSPHERE_VISUALS_DATA", {})
        gradient = visuals.get("GRADIENT", {})
        self.add_label_entry("Gradient Position Z", "gradient_positionZ", gradient)
        self.add_label_entry("Gradient Height", "gradient_height", gradient)
        self.add_label_entry("Gradient Texture", "gradient_texture", gradient)

    def add_label_entry(self, label_text, key, data_dict):
        ctk.CTkLabel(self.frame, text=label_text).pack(anchor="w", padx=5, pady=2)
        var = ctk.StringVar(value=str(data_dict.get(key, "")))
        entry = ctk.CTkEntry(self.frame, textvariable=var)
        entry.pack(fill="x", padx=5, pady=2)
        self.entries[key] = var

    def save(self):
        phys = self.planet_data.setdefault("ATMOSPHERE_PHYSICS_DATA", {})
        phys["height"] = float(self.entries.get("height", "0").get())
        phys["density"] = float(self.entries.get("density", "0").get())
        phys["curve"] = float(self.entries.get("curve", "0").get())
        phys["parachuteMultiplier"] = float(self.entries.get("parachuteMultiplier", "0").get())
        phys["upperAtmosphere"] = float(self.entries.get("upperAtmosphere", "0").get())
        phys["shockwaveIntensity"] = float(self.entries.get("shockwaveIntensity", "0").get())
        phys["minHeatingVelocityMultiplier"] = float(self.entries.get("minHeatingVelocityMultiplier", "0").get())

        visuals = self.planet_data.setdefault("ATMOSPHERE_VISUALS_DATA", {})
        gradient = visuals.setdefault("GRADIENT", {})
        gradient["positionZ"] = float(self.entries.get("gradient_positionZ", "0").get())
        gradient["height"] = float(self.entries.get("gradient_height", "0").get())
        gradient["texture"] = self.entries.get("gradient_texture", "").get()

    def get_data(self):
        phys = self.planet_data.get("ATMOSPHERE_PHYSICS_DATA", {})
        visuals = self.planet_data.get("ATMOSPHERE_VISUALS_DATA", {})

        # Physics Data
        physics_data = {
            "height": float(self.entries.get("height", ctk.StringVar(value=0)).get() or 0),
            "density": float(self.entries.get("density", ctk.StringVar(value=0)).get() or 0),
            "curve": float(self.entries.get("curve", ctk.StringVar(value=0)).get() or 0),
            "parachuteMultiplier": float(self.entries.get("parachuteMultiplier", ctk.StringVar(value=1)).get() or 1),
            "upperAtmosphere": float(self.entries.get("upperAtmosphere", ctk.StringVar(value=0.333)).get() or 0.333),
            "shockwaveIntensity": float(self.entries.get("shockwaveIntensity", ctk.StringVar(value=1)).get() or 1),
            "minHeatingVelocityMultiplier": float(self.entries.get("minHeatingVelocityMultiplier", ctk.StringVar(value=1)).get() or 1)
        }

        # Visuals Data (Gradient only for now)
        gradient_data = {
            "positionZ": float(self.entries.get("gradient_positionZ", ctk.StringVar(value=4000)).get() or 4000),
            "height": float(self.entries.get("gradient_height", ctk.StringVar(value=45000)).get() or 45000),
            "texture": self.entries.get("gradient_texture", ctk.StringVar(value="Atmo_Earth")).get()
        }

        return {
            "ATMOSPHERE_PHYSICS_DATA": physics_data,
            "ATMOSPHERE_VISUALS_DATA": {
                "GRADIENT": gradient_data
            }
        }
