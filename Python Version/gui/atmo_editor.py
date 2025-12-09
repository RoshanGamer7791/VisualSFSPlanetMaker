import customtkinter as ctk
import json
from tkinter import messagebox


class AtmosphereEditor(ctk.CTkToplevel):
    def __init__(self, master, data):
        super().__init__(master)
        self.title("Atmosphere Editor")
        self.geometry("720x750")

        self.data = data

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.build_ui()


    # -----------------------------------------------------
    # UI Builder
    # -----------------------------------------------------
    def build_ui(self):
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.scroll, text="ATMOSPHERE PHYSICS", font=("Arial", 18)).pack(pady=10)

        phys = self.data["ATMOSPHERE_PHYSICS_DATA"]
        self.height = self._entry("Height", phys.get("height"))
        self.density = self._entry("Density", phys.get("density"))
        self.curve = self._entry("Curve", phys.get("curve"))
        self.parachuteMultiplier = self._entry("Parachute Multiplier", phys.get("parachuteMultiplier"))
        self.upperAtmosphere = self._entry("Upper Atmosphere", phys.get("upperAtmosphere"))
        self.shockwaveIntensity = self._entry("Shockwave Intensity", phys.get("shockwaveIntensity"))
        self.minHeatingVelocity = self._entry("Min Heating Velocity Multiplier", phys.get("minHeatingVelocityMultiplier"))

        # dict textboxes
        self.curveScale_text = self._textbox("curveScale", phys.get("curveScale", {}))
        self.heightDifficulty_text = self._textbox("heightDifficultyScale", phys.get("heightDifficultyScale", {}))

        # -----------------------------------------------------
        # VISUALS
        # -----------------------------------------------------
        ctk.CTkLabel(self.scroll, text="ATMOSPHERE VISUALS", font=("Arial", 18)).pack(pady=10)

        visuals = self.data["ATMOSPHERE_VISUALS_DATA"]

        # --- GRADIENT ---
        grad = visuals["GRADIENT"]
        self.gradient_positionZ = self._entry("Gradient positionZ (INTEGER)", grad.get("positionZ"))
        self.gradient_height = self._entry("Gradient Height", grad.get("height"))
        self.gradient_texture = self._entry("Gradient Texture", grad.get("texture"))

        # --- CLOUDS ---
        clouds = visuals["CLOUDS"]
        self.cloud_tex = self._entry("Cloud Texture", clouds.get("texture"))
        self.cloud_startHeight = self._entry("Cloud Start Height", clouds.get("startHeight"))
        self.cloud_width = self._entry("Cloud Width", clouds.get("width"))
        self.cloud_height = self._entry("Cloud Height", clouds.get("height"))
        self.cloud_alpha = self._entry("Cloud Alpha", clouds.get("alpha"))
        self.cloud_velocity = self._entry("Cloud Velocity", clouds.get("velocity"))

        # --- FOG ---
        ctk.CTkLabel(self.scroll, text="Fog Keys", font=("Arial", 15)).pack(pady=5)

        self.fog_entries = []
        for key in visuals["FOG"].get("keys", []):
            self._add_fog_key(key)

        ctk.CTkButton(self.scroll, text="Add Fog Key", command=self._add_empty_fog).pack(pady=5)


    # -----------------------------------------------------
    # Helper methods
    # -----------------------------------------------------
    def _entry(self, label, value):
        frame = ctk.CTkFrame(self.scroll)
        frame.pack(fill="x", pady=4)

        ctk.CTkLabel(frame, text=label).pack(side="left", padx=5)
        ent = ctk.CTkEntry(frame)
        ent.pack(side="right", fill="x", expand=True, padx=5)
        ent.insert(0, str(value))

        return ent

    def _textbox(self, label, data_dict):
        frame = ctk.CTkFrame(self.scroll)
        frame.pack(fill="x", pady=4)

        ctk.CTkLabel(frame, text=label).pack(anchor="w", padx=5)

        box = ctk.CTkTextbox(frame, height=80)
        box.pack(fill="x", padx=5)
        box.insert("0.0", json.dumps(data_dict, indent=2))

        return box

    def _add_fog_key(self, key):
        frame = ctk.CTkFrame(self.scroll)
        frame.pack(fill="x", pady=4)

        color = key["color"]
        r = self._entry("R", color["r"])
        g = self._entry("G", color["g"])
        b = self._entry("B", color["b"])
        a = self._entry("A", color["a"])
        dist = self._entry("Distance", key["distance"])

        self.fog_entries.append((r, g, b, a, dist))

    def _add_empty_fog(self):
        self._add_fog_key({
            "color": {"r": 1, "g": 1, "b": 1, "a": 1},
            "distance": 0
        })


    # -----------------------------------------------------
    # get_data()
    # -----------------------------------------------------
    def get_data(self):
        try:
            positionZ_int = int(self.gradient_positionZ.get())
        except:
            messagebox.showerror("Error", "positionZ must be an INTEGER!")
            return None

        # parse dicts
        try:
            curveScale_dict = json.loads(self.curveScale_text.get("0.0", "end"))
            heightDifficulty_dict = json.loads(self.heightDifficulty_text.get("0.0", "end"))
        except:
            messagebox.showerror("Error", "curveScale or heightDifficultyScale must contain valid JSON!")
            return None

        fog_list = []
        for r, g, b, a, dist in self.fog_entries:
            fog_list.append({
                "color": {
                    "r": float(r.get()),
                    "g": float(g.get()),
                    "b": float(b.get()),
                    "a": float(a.get())
                },
                "distance": float(dist.get())
            })

        return {
            "ATMOSPHERE_PHYSICS_DATA": {
                "height": float(self.height.get()),
                "density": float(self.density.get()),
                "curve": float(self.curve.get()),
                "curveScale": curveScale_dict,
                "parachuteMultiplier": float(self.parachuteMultiplier.get()),
                "upperAtmosphere": float(self.upperAtmosphere.get()),
                "heightDifficultyScale": heightDifficulty_dict,
                "shockwaveIntensity": float(self.shockwaveIntensity.get()),
                "minHeatingVelocityMultiplier": float(self.minHeatingVelocity.get()),
            },
            "ATMOSPHERE_VISUALS_DATA": {
                "GRADIENT": {
                    "positionZ": positionZ_int,
                    "height": float(self.gradient_height.get()),
                    "texture": self.gradient_texture.get()
                },
                "CLOUDS": {
                    "texture": self.cloud_tex.get(),
                    "startHeight": float(self.cloud_startHeight.get()),
                    "width": float(self.cloud_width.get()),
                    "height": float(self.cloud_height.get()),
                    "alpha": float(self.cloud_alpha.get()),
                    "velocity": float(self.cloud_velocity.get())
                },
                "FOG": {
                    "keys": fog_list
                }
            }
        }
