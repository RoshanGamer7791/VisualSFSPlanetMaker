import customtkinter as ctk
from tkinter import colorchooser

class PlanetPropertiesEditor:
    def __init__(self, parent_frame, planet_data):
        self.planet_data = planet_data
        self.frame = ctk.CTkFrame(parent_frame)
        self.frame.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self.frame, text="Planet Properties Editor", font=("Segoe UI", 18, "bold"))
        title.pack(pady=10)

        # --------------------- Radius ---------------------
        radius_frame = ctk.CTkFrame(self.frame)
        radius_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(radius_frame, text="Radius (m):").pack(side="left", padx=5)
        self.radius_entry = ctk.CTkEntry(radius_frame, width=100)
        self.radius_entry.pack(side="left", padx=5)
        self.radius_entry.insert(0, str(self.planet_data.get("BASE_DATA", {}).get("radius", 0.0)))

        # --------------------- Gravity ---------------------
        gravity_frame = ctk.CTkFrame(self.frame)
        gravity_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(gravity_frame, text="Gravity (m/s²):").pack(side="left", padx=5)
        self.gravity_entry = ctk.CTkEntry(gravity_frame, width=100)
        self.gravity_entry.pack(side="left", padx=5)
        self.gravity_entry.insert(0, str(self.planet_data.get("BASE_DATA", {}).get("gravity", 0.0)))

        # --------------------- Timewarp Height ---------------------
        tw_frame = ctk.CTkFrame(self.frame)
        tw_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(tw_frame, text="Timewarp Height (m):").pack(side="left", padx=5)
        self.timewarp_entry = ctk.CTkEntry(tw_frame, width=100)
        self.timewarp_entry.pack(side="left", padx=5)
        self.timewarp_entry.insert(0, str(self.planet_data.get("BASE_DATA", {}).get("timewarpHeight", 0.0)))

        # --------------------- Velocity Arrows Height ---------------------
        va_frame = ctk.CTkFrame(self.frame)
        va_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(va_frame, text="Velocity Arrows Height (m):").pack(side="left", padx=5)
        self.va_entry = ctk.CTkEntry(va_frame, width=100)
        self.va_entry.pack(side="left", padx=5)
        self.va_entry.insert(0, str(self.planet_data.get("BASE_DATA", {}).get("velocityArrowsHeight", 0.0)))

        # --------------------- Map Color ---------------------
        color_frame = ctk.CTkFrame(self.frame)
        color_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(color_frame, text="Map Color:").pack(side="left", padx=5)
        self.map_color_btn = ctk.CTkButton(color_frame, text="Pick Color", command=self.pick_color)
        self.map_color_btn.pack(side="left", padx=5)

        base_map_color = self.planet_data.get("BASE_DATA", {}).get("mapColor", {"r":1,"g":1,"b":1,"a":1})
        self.map_color = (
            int(base_map_color.get("r",1)*255),
            int(base_map_color.get("g",1)*255),
            int(base_map_color.get("b",1)*255)
        )

    # --------------------- Pick Color ---------------------
    def pick_color(self):
        rgb_color, _ = colorchooser.askcolor(color=self.map_color)
        if rgb_color:
            self.map_color = tuple(int(c) for c in rgb_color)

    # --------------------- Export Data ---------------------
    def get_data(self):
        r, g, b = [c/255.0 for c in self.map_color]
        return {
            "BASE_DATA": {
                "radius": float(self.radius_entry.get()),
                "radiusDifficultyScale": {},
                "gravity": float(self.gravity_entry.get()),
                "gravityDifficultyScale": {},
                "timewarpHeight": float(self.timewarp_entry.get()),
                "velocityArrowsHeight": float(self.va_entry.get()),
                "mapColor": {"r": r, "g": g, "b": b, "a": 1.0},
                "significant": True,
                "rotateCamera": True
            }
        }
