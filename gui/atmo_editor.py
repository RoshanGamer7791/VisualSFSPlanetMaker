# gui/atmosphere_editor.py
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser

class AtmosphereEditor(tk.Frame):
    def __init__(self, master, planet_data):
        super().__init__(master)
        self.master = master
        self.planet_data = planet_data
        if "ATMOSPHERE_PHYSICS_DATA" not in self.planet_data:
            self.planet_data["ATMOSPHERE_PHYSICS_DATA"] = {}
        if "ATMOSPHERE_VISUALS_DATA" not in self.planet_data:
            self.planet_data["ATMOSPHERE_VISUALS_DATA"] = {}
        self.create_widgets()

    def create_widgets(self):
        phys = self.planet_data["ATMOSPHERE_PHYSICS_DATA"]
        vis = self.planet_data["ATMOSPHERE_VISUALS_DATA"]

        # Physics
        tk.Label(self, text="Height:").grid(row=0, column=0, sticky="e")
        self.entry_height = tk.Entry(self)
        self.entry_height.insert(0, str(phys.get("height", 0)))
        self.entry_height.grid(row=0, column=1)

        tk.Label(self, text="Density:").grid(row=1, column=0, sticky="e")
        self.entry_density = tk.Entry(self)
        self.entry_density.insert(0, str(phys.get("density", 0)))
        self.entry_density.grid(row=1, column=1)

        tk.Label(self, text="Curve:").grid(row=2, column=0, sticky="e")
        self.entry_curve = tk.Entry(self)
        self.entry_curve.insert(0, str(phys.get("curve", 0)))
        self.entry_curve.grid(row=2, column=1)

        tk.Label(self, text="Curve Scale:").grid(row=3, column=0, sticky="e")
        self.entry_curve_scale = tk.Entry(self)
        self.entry_curve_scale.insert(0, str(phys.get("curveScale", {})))
        self.entry_curve_scale.grid(row=3, column=1)

        tk.Label(self, text="Parachute Multiplier:").grid(row=4, column=0, sticky="e")
        self.entry_parachute = tk.Entry(self)
        self.entry_parachute.insert(0, str(phys.get("parachuteMultiplier", 1.0)))
        self.entry_parachute.grid(row=4, column=1)

        tk.Label(self, text="Upper Atmosphere:").grid(row=5, column=0, sticky="e")
        self.entry_upper = tk.Entry(self)
        self.entry_upper.insert(0, str(phys.get("upperAtmosphere", 0)))
        self.entry_upper.grid(row=5, column=1)

        tk.Label(self, text="Shockwave Intensity:").grid(row=6, column=0, sticky="e")
        self.entry_shockwave = tk.Entry(self)
        self.entry_shockwave.insert(0, str(phys.get("shockwaveIntensity", 1.0)))
        self.entry_shockwave.grid(row=6, column=1)

        tk.Label(self, text="Min Heating Velocity Multiplier:").grid(row=7, column=0, sticky="e")
        self.entry_min_heat = tk.Entry(self)
        self.entry_min_heat.insert(0, str(phys.get("minHeatingVelocityMultiplier", 1.0)))
        self.entry_min_heat.grid(row=7, column=1)

        # Visuals
        tk.Label(self, text="Gradient Texture:").grid(row=8, column=0, sticky="e")
        self.entry_grad_texture = tk.Entry(self)
        self.entry_grad_texture.insert(0, vis.get("GRADIENT", {}).get("texture", ""))
        self.entry_grad_texture.grid(row=8, column=1)

        tk.Label(self, text="Gradient Height:").grid(row=9, column=0, sticky="e")
        self.entry_grad_height = tk.Entry(self)
        self.entry_grad_height.insert(0, str(vis.get("GRADIENT", {}).get("height", 0)))
        self.entry_grad_height.grid(row=9, column=1)

        tk.Label(self, text="Gradient PositionZ:").grid(row=10, column=0, sticky="e")
        self.entry_grad_posz = tk.Entry(self)
        self.entry_grad_posz.insert(0, str(vis.get("GRADIENT", {}).get("positionZ", 0)))
        self.entry_grad_posz.grid(row=10, column=1)

        # Clouds
        clouds = vis.get("CLOUDS", {})
        tk.Label(self, text="Cloud Texture:").grid(row=11, column=0, sticky="e")
        self.entry_cloud_texture = tk.Entry(self)
        self.entry_cloud_texture.insert(0, clouds.get("texture", ""))
        self.entry_cloud_texture.grid(row=11, column=1)

        tk.Label(self, text="Cloud Start Height:").grid(row=12, column=0, sticky="e")
        self.entry_cloud_start = tk.Entry(self)
        self.entry_cloud_start.insert(0, str(clouds.get("startHeight", 0)))
        self.entry_cloud_start.grid(row=12, column=1)

        tk.Label(self, text="Cloud Width:").grid(row=13, column=0, sticky="e")
        self.entry_cloud_width = tk.Entry(self)
        self.entry_cloud_width.insert(0, str(clouds.get("width", 0)))
        self.entry_cloud_width.grid(row=13, column=1)

        tk.Label(self, text="Cloud Height:").grid(row=14, column=0, sticky="e")
        self.entry_cloud_height = tk.Entry(self)
        self.entry_cloud_height.insert(0, str(clouds.get("height", 0)))
        self.entry_cloud_height.grid(row=14, column=1)

        tk.Label(self, text="Cloud Alpha:").grid(row=15, column=0, sticky="e")
        self.entry_cloud_alpha = tk.Entry(self)
        self.entry_cloud_alpha.insert(0, str(clouds.get("alpha", 0)))
        self.entry_cloud_alpha.grid(row=15, column=1)

        tk.Label(self, text="Cloud Velocity:").grid(row=16, column=0, sticky="e")
        self.entry_cloud_vel = tk.Entry(self)
        self.entry_cloud_vel.insert(0, str(clouds.get("velocity", 0)))
        self.entry_cloud_vel.grid(row=16, column=1)

        # TODO: You can add fog editor later if needed

    def update_planet_data(self):
        phys = self.planet_data["ATMOSPHERE_PHYSICS_DATA"]
        vis = self.planet_data["ATMOSPHERE_VISUALS_DATA"]

        try:
            phys["height"] = float(self.entry_height.get())
            phys["density"] = float(self.entry_density.get())
            phys["curve"] = float(self.entry_curve.get())
            phys["curveScale"] = eval(self.entry_curve_scale.get())
            phys["parachuteMultiplier"] = float(self.entry_parachute.get())
            phys["upperAtmosphere"] = float(self.entry_upper.get())
            phys["shockwaveIntensity"] = float(self.entry_shockwave.get())
            phys["minHeatingVelocityMultiplier"] = float(self.entry_min_heat.get())

            vis.setdefault("GRADIENT", {})
            vis["GRADIENT"]["texture"] = self.entry_grad_texture.get()
            vis["GRADIENT"]["height"] = float(self.entry_grad_height.get())
            vis["GRADIENT"]["positionZ"] = float(self.entry_grad_posz.get())

            vis.setdefault("CLOUDS", {})
            vis["CLOUDS"]["texture"] = self.entry_cloud_texture.get()
            vis["CLOUDS"]["startHeight"] = float(self.entry_cloud_start.get())
            vis["CLOUDS"]["width"] = float(self.entry_cloud_width.get())
            vis["CLOUDS"]["height"] = float(self.entry_cloud_height.get())
            vis["CLOUDS"]["alpha"] = float(self.entry_cloud_alpha.get())
            vis["CLOUDS"]["velocity"] = float(self.entry_cloud_vel.get())

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
