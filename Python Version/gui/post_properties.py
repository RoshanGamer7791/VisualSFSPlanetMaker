import customtkinter as ctk
from tkinter import messagebox


class PostProcessingEditor:
    def __init__(self, master, data):
        # Main container frame (required by main.py)
        self.frame = ctk.CTkFrame(master)
        
        self.data = data if isinstance(data, dict) else {}
        self.key_entries = []

        self.build_ui()


    # ---------------------------------------------------------
    # UI BUILD
    # ---------------------------------------------------------
    def build_ui(self):
        ctk.CTkLabel(
            self.frame, text="POST PROCESSING KEYS",
            font=("Arial", 20)
        ).pack(pady=10)

        # Scroll panel
        self.scroll = ctk.CTkScrollableFrame(self.frame)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Load existing keys
        for key in self.data.get("keys", []):
            self.add_key_block(key)

        # Add key button
        ctk.CTkButton(self.frame, text="Add Key", command=self.add_empty_key).pack(pady=10)


    # ---------------------------------------------------------
    # Helper entry row
    # ---------------------------------------------------------
    def _entry(self, frame, label, value):
        row = ctk.CTkFrame(frame)
        row.pack(fill="x", pady=2)

        ctk.CTkLabel(row, text=label, width=140, anchor="w").pack(side="left", padx=5)

        entry = ctk.CTkEntry(row)
        entry.pack(side="right", fill="x", expand=True, padx=5)
        if value is not None:
            entry.insert(0, str(value))

        return entry


    # ---------------------------------------------------------
    # Add Key Block
    # ---------------------------------------------------------
    def add_key_block(self, key):
        frame = ctk.CTkFrame(self.scroll, border_width=1, border_color="#333")
        frame.pack(fill="x", pady=10, padx=5)

        height = self._entry(frame, "Height", key.get("height"))
        shadow = self._entry(frame, "Shadow Intensity", key.get("shadowIntensity"))
        star = self._entry(frame, "Star Intensity", key.get("starIntensity"))
        hue = self._entry(frame, "Hue Shift", key.get("hueShift"))
        sat = self._entry(frame, "Saturation", key.get("saturation"))
        cont = self._entry(frame, "Contrast", key.get("contrast"))
        red = self._entry(frame, "Red", key.get("red"))
        green = self._entry(frame, "Green", key.get("green"))
        blue = self._entry(frame, "Blue", key.get("blue"))

        remove_btn = ctk.CTkButton(
            frame, text="Remove", fg_color="#992222",
            command=lambda f=frame: self.remove_block(f)
        )
        remove_btn.pack(pady=5)

        self.key_entries.append(
            (frame, height, shadow, star, hue, sat, cont, red, green, blue)
        )


    def add_empty_key(self):
        self.add_key_block({
            "height": 0.0,
            "shadowIntensity": 1.0,
            "starIntensity": 0.0,
            "hueShift": 0.0,
            "saturation": 1.0,
            "contrast": 1.0,
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        })


    # ---------------------------------------------------------
    # Remove a block
    # ---------------------------------------------------------
    def remove_block(self, frame):
        for block in self.key_entries:
            if block[0] == frame:
                block[0].destroy()
                self.key_entries.remove(block)
                return


    # ---------------------------------------------------------
    # get_data() — used by main.py
    # ---------------------------------------------------------
    def get_data(self):
        output = {"keys": []}

        for block in self.key_entries:
            (_, height, shadow, star, hue, sat, cont, red, green, blue) = block

            # Skip blank blocks
            if all(e.get().strip() == "" for e in
                   (height, shadow, star, hue, sat, cont, red, green, blue)):
                continue

            try:
                output["keys"].append({
                    "height": float(height.get()),
                    "shadowIntensity": float(shadow.get()),
                    "starIntensity": float(star.get()),
                    "hueShift": float(hue.get()),
                    "saturation": float(sat.get()),
                    "contrast": float(cont.get()),
                    "red": float(red.get()),
                    "green": float(green.get()),
                    "blue": float(blue.get())
                })
            except:
                messagebox.showerror(
                    "Error", "POST PROCESSING contains invalid number(s)."
                )
                return {}   # return empty dict so update() does not fail

        # If no keys → do NOT include POST_PROCESSING in file
        if len(output["keys"]) == 0:
            return {}  # SAFE for update()

        # Wrap in POST_PROCESSING
        return {"POST_PROCESSING": output}
