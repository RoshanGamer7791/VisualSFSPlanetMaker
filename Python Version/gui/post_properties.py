import customtkinter as ctk

class PostProcessingEditor:
    def __init__(self, parent_frame, planet_data):
        self.planet_data = planet_data
        self.frame = ctk.CTkFrame(parent_frame)
        self.frame.pack(fill="both", expand=True)

        self.key_frames = []
        self.keys_data = planet_data.get("POST_PROCESSING", {}).get("keys", [])

        title = ctk.CTkLabel(self.frame, text="Post-Processing Editor", font=("Segoe UI", 18, "bold"))
        title.pack(pady=10)

        # Scrollable area for key entries
        self.scroll = ctk.CTkScrollableFrame(self.frame, width=600, height=500)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self.frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Add Key", command=self.add_key).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Clear All", command=self.clear_all).grid(row=0, column=1, padx=5)

        # Load existing keys
        for key in self.keys_data:
            self.create_key_widget(key)

    # -------------------------
    # Create a single key section
    # -------------------------
    def create_key_widget(self, key):
        box = ctk.CTkFrame(self.scroll, corner_radius=10)
        box.pack(fill="x", pady=8, padx=5)

        title = ctk.CTkLabel(box, text=f"Key (Height: {key.get('height', 0)})", font=("Segoe UI", 14, "bold"))
        title.pack(pady=5)

        entries = {}

        def add_field(label_text, key_name):
            row = ctk.CTkFrame(box)
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=label_text, width=160, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row)
            entry.pack(side="left", fill="x", expand=True, padx=5)
            entry.insert(0, str(key.get(key_name, 0)))
            entries[key_name] = entry

        # Numeric fields
        add_field("Height", "height")
        add_field("Shadow Intensity", "shadowIntensity")
        add_field("Star Intensity", "starIntensity")
        add_field("Hue Shift", "hueShift")
        add_field("Saturation", "saturation")
        add_field("Contrast", "contrast")
        add_field("Red", "red")
        add_field("Green", "green")
        add_field("Blue", "blue")

        # Remove button
        def remove_key():
            box.destroy()
            self.key_frames.remove((box, entries))

        remove_btn = ctk.CTkButton(box, text="Remove Key", fg_color="#aa3333", command=remove_key)
        remove_btn.pack(pady=5)

        self.key_frames.append((box, entries))

    # ---------------------------------
    # Add a new blank key
    # ---------------------------------
    def add_key(self):
        blank_key = {
            "height": 0.0,
            "shadowIntensity": 1.0,
            "starIntensity": 0.0,
            "hueShift": 0.0,
            "saturation": 1.0,
            "contrast": 1.0,
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        }
        self.create_key_widget(blank_key)

    # ---------------------------------
    # Clear all keys
    # ---------------------------------
    def clear_all(self):
        for frame, _ in self.key_frames:
            frame.destroy()
        self.key_frames = []

    # ---------------------------------
    # Export data to JSON for SFS
    # ---------------------------------
    def get_data(self):
        """
        Return POST_PROCESSING structure for SFS exporter.
        Always returns a dict. Returns empty dict if no keys.
        """
        keys_out = []

        for frame, entries in self.key_frames:
            try:
                keys_out.append({
                    "height": float(entries["height"].get()),
                    "shadowIntensity": float(entries["shadowIntensity"].get()),
                    "starIntensity": float(entries["starIntensity"].get()),
                    "hueShift": float(entries["hueShift"].get()),
                    "saturation": float(entries["saturation"].get()),
                    "contrast": float(entries["contrast"].get()),
                    "red": float(entries["red"].get()),
                    "green": float(entries["green"].get()),
                    "blue": float(entries["blue"].get())
                })
            except ValueError:
                print("Warning: invalid post-processing value")

        if keys_out:
            return {"POST_PROCESSING": {"keys": keys_out}}
        else:
            return {}  # Safe for data.update()
