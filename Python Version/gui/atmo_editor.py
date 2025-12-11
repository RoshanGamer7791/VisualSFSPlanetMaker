import customtkinter as ctk

class AtmosphereEditor:
    def __init__(self, parent, planet_data=None):
        self.planet_data = planet_data or {}
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        # ------------------- Physics -------------------
        atm_phys = self.planet_data.get("ATMOSPHERE_PHYSICS_DATA", {})
        self.height = ctk.DoubleVar(value=atm_phys.get("height", 30000.0))
        self.density = ctk.DoubleVar(value=atm_phys.get("density", 0.005))
        self.curve = ctk.DoubleVar(value=atm_phys.get("curve", 10.0))
        self.parachuteMultiplier = ctk.DoubleVar(value=atm_phys.get("parachuteMultiplier", 1.0))
        self.upperAtmosphere = ctk.DoubleVar(value=atm_phys.get("upperAtmosphere", 0.333))
        self.shockwaveIntensity = ctk.DoubleVar(value=atm_phys.get("shockwaveIntensity", 1.0))
        self.minHeatingVelocityMultiplier = ctk.DoubleVar(value=atm_phys.get("minHeatingVelocityMultiplier", 1.0))

        # ------------------- Gradient -------------------
        visuals = self.planet_data.get("ATMOSPHERE_VISUALS_DATA", {})
        grad = visuals.get("GRADIENT", {})
        self.gradientTexture = ctk.StringVar(value=grad.get("texture", "Atmo_Earth"))
        self.gradientHeight = ctk.DoubleVar(value=grad.get("height", 45000.0))
        self.gradientPositionZ = ctk.DoubleVar(value=grad.get("positionZ", 4000))

        # ------------------- Clouds -------------------
        clouds = visuals.get("CLOUDS", {})
        self.cloudTexture = ctk.StringVar(value=clouds.get("texture", "Earth_Clouds"))
        self.cloudStartHeight = ctk.DoubleVar(value=clouds.get("startHeight", 1200.0))
        self.cloudWidth = ctk.DoubleVar(value=clouds.get("width", 40845.87))
        self.cloudHeight = ctk.DoubleVar(value=clouds.get("height", 36000.0))
        self.cloudAlpha = ctk.DoubleVar(value=clouds.get("alpha", 0.1))
        self.cloudVelocity = ctk.DoubleVar(value=clouds.get("velocity", 2.0))

        # ------------------- Fog -------------------
        fog = visuals.get("FOG", {}).get("keys", [])
        self.fogKeys = []
        self.fogFrame = ctk.CTkFrame(self.frame)
        self.fogFrame.grid(row=20, column=0, columnspan=2, sticky="nsew")
        self.fogRowStart = 0

        for key in fog:
            color = key.get("color", {})
            self.add_fog_key({
                "r": color.get("r", 0.647058845),
                "g": color.get("g", 0.848739564),
                "b": color.get("b", 1.0),
                "a": color.get("a", 0.416),
                "distance": key.get("distance", 30000.0)
            })

        # Add button to add more fog keys
        self.addFogButton = ctk.CTkButton(self.frame, text="Add Fog Key", command=self.add_fog_key)
        self.addFogButton.grid(row=99, column=0, columnspan=2, pady=10)

        self.build_ui()

    def build_ui(self):
        row = 0
        # Physics
        for label, var in [
            ("Atmosphere Height", self.height),
            ("Density", self.density),
            ("Curve", self.curve),
            ("Parachute Multiplier", self.parachuteMultiplier),
            ("Upper Atmosphere", self.upperAtmosphere),
            ("Shockwave Intensity", self.shockwaveIntensity),
            ("Min Heating Velocity Multiplier", self.minHeatingVelocityMultiplier)
        ]:
            ctk.CTkLabel(self.frame, text=label).grid(row=row, column=0)
            ctk.CTkEntry(self.frame, textvariable=var).grid(row=row, column=1)
            row += 1

        # Gradient
        for label, var in [
            ("Gradient Texture", self.gradientTexture),
            ("Gradient Height", self.gradientHeight),
            ("Gradient PositionZ", self.gradientPositionZ)
        ]:
            ctk.CTkLabel(self.frame, text=label).grid(row=row, column=0)
            ctk.CTkEntry(self.frame, textvariable=var).grid(row=row, column=1)
            row += 1

        # Clouds
        ctk.CTkLabel(self.frame, text="--- Clouds ---").grid(row=row, column=0, columnspan=2)
        row += 1
        for label, var in [
            ("Texture", self.cloudTexture),
            ("Start Height", self.cloudStartHeight),
            ("Width", self.cloudWidth),
            ("Height", self.cloudHeight),
            ("Alpha", self.cloudAlpha),
            ("Velocity", self.cloudVelocity)
        ]:
            ctk.CTkLabel(self.frame, text=label).grid(row=row, column=0)
            ctk.CTkEntry(self.frame, textvariable=var).grid(row=row, column=1)
            row += 1

        # Fog label
        ctk.CTkLabel(self.frame, text="--- Fog Keys ---").grid(row=row, column=0, columnspan=2)
        row += 1

        # Build initial fog keys
        for key in self.fogKeys:
            self.render_fog_key(key)

    def add_fog_key(self, default=None):
        if default is None:
            default = {"r":0.647058845,"g":0.848739564,"b":1.0,"a":0.416,"distance":30000.0}
        key = {
            "r": ctk.DoubleVar(value=default["r"]),
            "g": ctk.DoubleVar(value=default["g"]),
            "b": ctk.DoubleVar(value=default["b"]),
            "a": ctk.DoubleVar(value=default["a"]),
            "distance": ctk.DoubleVar(value=default["distance"])
        }
        self.fogKeys.append(key)
        self.render_fog_key(key)

    def remove_fog_key(self, key):
        for widget in key["widgets"]:
            widget.destroy()
        self.fogKeys.remove(key)

    def render_fog_key(self, key):
        key["widgets"] = []
        row = self.fogRowStart
        ctk.CTkLabel(self.fogFrame, text=f"Fog Key {len(self.fogKeys)}").grid(row=row, column=0, columnspan=2)
        key["widgets"].append(self.fogFrame)
        row += 1
        for label, var in [("R", key["r"]), ("G", key["g"]), ("B", key["b"]), ("A", key["a"]), ("Distance", key["distance"])]:
            lbl = ctk.CTkLabel(self.fogFrame, text=label)
            lbl.grid(row=row, column=0)
            entry = ctk.CTkEntry(self.fogFrame, textvariable=var)
            entry.grid(row=row, column=1)
            key["widgets"].extend([lbl, entry])
            row += 1
        # Remove button
        btn = ctk.CTkButton(self.fogFrame, text="Remove", command=lambda k=key: self.remove_fog_key(k))
        btn.grid(row=row, column=0, columnspan=2, pady=5)
        key["widgets"].append(btn)
        self.fogRowStart = row + 1

    def get_data(self):
        return {
            "ATMOSPHERE_PHYSICS_DATA": {
                "height": self.height.get(),
                "density": self.density.get(),
                "curve": self.curve.get(),
                "curveScale": {},
                "parachuteMultiplier": self.parachuteMultiplier.get(),
                "upperAtmosphere": self.upperAtmosphere.get(),
                "heightDifficultyScale": {},
                "shockwaveIntensity": self.shockwaveIntensity.get(),
                "minHeatingVelocityMultiplier": self.minHeatingVelocityMultiplier.get()
            },
            "ATMOSPHERE_VISUALS_DATA": {
                "GRADIENT": {
                    "positionZ": self.gradientPositionZ.get(),
                    "height": self.gradientHeight.get(),
                    "texture": self.gradientTexture.get()
                },
                "CLOUDS": {
                    "texture": self.cloudTexture.get(),
                    "startHeight": self.cloudStartHeight.get(),
                    "width": self.cloudWidth.get(),
                    "height": self.cloudHeight.get(),
                    "alpha": self.cloudAlpha.get(),
                    "velocity": self.cloudVelocity.get()
                },
                "FOG": {
                    "keys": [
                        {
                            "color": {
                                "r": k["r"].get(),
                                "g": k["g"].get(),
                                "b": k["b"].get(),
                                "a": k["a"].get()
                            },
                            "distance": k["distance"].get()
                        } for k in self.fogKeys
                    ]
                }
            }
        }
