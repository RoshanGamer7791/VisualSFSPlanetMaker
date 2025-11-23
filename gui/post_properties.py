import customtkinter as ctk

class PostProcessingEditor:
    def __init__(self, parent, planet_data):
        self.parent = parent
        self.planet_data = planet_data
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        post = self.planet_data.get("POST_PROCESSING", {})
        self.keys = post.get("keys", [])

        self.key_frames = []

        for i, key in enumerate(self.keys):
            frame = ctk.CTkFrame(self.frame, corner_radius=10, border_width=1)
            frame.pack(fill="x", padx=10, pady=5)
            self.key_frames.append(frame)

            # Height
            height_var = ctk.StringVar(value=str(key.get("height", 0)))
            ctk.CTkLabel(frame, text=f"Key {i} Height").grid(row=0, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkEntry(frame, textvariable=height_var).grid(row=0, column=1, padx=5, pady=2)
            key["height_var"] = height_var

            # Shadow Intensity
            shadow_var = ctk.StringVar(value=str(key.get("shadowIntensity", 0)))
            ctk.CTkLabel(frame, text="Shadow Intensity").grid(row=1, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkEntry(frame, textvariable=shadow_var).grid(row=1, column=1, padx=5, pady=2)
            key["shadow_var"] = shadow_var

            # Star Intensity
            star_var = ctk.StringVar(value=str(key.get("starIntensity", 0)))
            ctk.CTkLabel(frame, text="Star Intensity").grid(row=2, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkEntry(frame, textvariable=star_var).grid(row=2, column=1, padx=5, pady=2)
            key["star_var"] = star_var

            # Saturation
            saturation_var = ctk.StringVar(value=str(key.get("saturation", 1)))
            ctk.CTkLabel(frame, text="Saturation").grid(row=3, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkEntry(frame, textvariable=saturation_var).grid(row=3, column=1, padx=5, pady=2)
            key["saturation_var"] = saturation_var

            # Contrast
            contrast_var = ctk.StringVar(value=str(key.get("contrast", 1)))
            ctk.CTkLabel(frame, text="Contrast").grid(row=4, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkEntry(frame, textvariable=contrast_var).grid(row=4, column=1, padx=5, pady=2)
            key["contrast_var"] = contrast_var

            # Hue Shift
            hue_var = ctk.StringVar(value=str(key.get("hueShift", 0)))
            ctk.CTkLabel(frame, text="Hue Shift").grid(row=5, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkEntry(frame, textvariable=hue_var).grid(row=5, column=1, padx=5, pady=2)
            key["hue_var"] = hue_var

            # Color
            color = key
            self.add_color_entry(frame, "Red", i, "red", color.get("red", 1))
            self.add_color_entry(frame, "Green", i, "green", color.get("green", 1))
            self.add_color_entry(frame, "Blue", i, "blue", color.get("blue", 1))

    def add_color_entry(self, frame, label, index, key, value):
        var = ctk.StringVar(value=str(value))
        row = 6 + ["red", "green", "blue"].index(key)
        ctk.CTkLabel(frame, text=label).grid(row=row, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkEntry(frame, textvariable=var).grid(row=row, column=1, padx=5, pady=2)
        self.keys[index][f"{key}_var"] = var

    def save(self):
        post = self.planet_data.setdefault("POST_PROCESSING", {})
        keys_data = []
        for key in self.keys:
            keys_data.append({
                "height": float(key["height_var"].get()),
                "shadowIntensity": float(key["shadow_var"].get()),
                "starIntensity": float(key["star_var"].get()),
                "saturation": float(key["saturation_var"].get()),
                "contrast": float(key["contrast_var"].get()),
                "hueShift": float(key["hue_var"].get()),
                "red": float(key["red_var"].get()),
                "green": float(key["green_var"].get()),
                "blue": float(key["blue_var"].get())
            })
        post["keys"] = keys_data

    def get_data(self):
        return {
            "POST_PROCESSING": {
                "keys": self.keys  # list of dicts
            }
        }

