import customtkinter as ctk

class LandmarksEditor:
    def __init__(self, parent, planet_data):
        self.parent = parent
        self.planet_data = planet_data
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True)
        self.landmark_entries = []
        self.build_ui()

    def build_ui(self):
        landmarks = self.planet_data.get("LANDMARKS", [])

        # Existing landmarks
        for lm in landmarks:
            self.add_landmark_ui(lm)

        # Add new landmark button
        ctk.CTkButton(self.frame, text="Add Landmark", command=lambda: self.add_landmark_ui()).pack(padx=5, pady=5)

    def add_landmark_ui(self, data=None):
        data = data or {"name": "", "angle": 0.0, "startAngle": 0.0, "endAngle": 0.0}
        f_frame = ctk.CTkFrame(self.frame)
        f_frame.pack(fill="x", padx=5, pady=2)

        name_var = ctk.StringVar(value=data.get("name", ""))
        angle_var = ctk.DoubleVar(value=data.get("angle", 0.0))
        start_var = ctk.DoubleVar(value=data.get("startAngle", 0.0))
        end_var = ctk.DoubleVar(value=data.get("endAngle", 0.0))

        for label, var in [("Name", name_var), ("Angle", angle_var), ("Start Angle", start_var), ("End Angle", end_var)]:
            ctk.CTkLabel(f_frame, text=label).pack(anchor="w", padx=5)
            ctk.CTkEntry(f_frame, textvariable=var).pack(fill="x", padx=5, pady=2)

        # Remove button
        ctk.CTkButton(f_frame, text="Remove", command=lambda: self.remove_landmark(f_frame)).pack(padx=5, pady=2, anchor="e")

        self.landmark_entries.append({
            "frame": f_frame,
            "name": name_var,
            "angle": angle_var,
            "startAngle": start_var,
            "endAngle": end_var
        })

    def remove_landmark(self, frame):
        for lm in self.landmark_entries:
            if lm["frame"] == frame:
                lm["frame"].destroy()
                self.landmark_entries.remove(lm)
                break

    def get_data(self):
        landmarks_list = []

        for lm in self.landmark_entries:
            landmarks_list.append({
                "name": lm["name"].get(),
                "angle": float(lm["angle"].get()),
                "startAngle": float(lm["startAngle"].get()),
                "endAngle": float(lm["endAngle"].get())
            })

        return {"LANDMARKS": landmarks_list}

