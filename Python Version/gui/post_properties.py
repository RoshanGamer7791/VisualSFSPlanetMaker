import customtkinter as ctk

class PostProcessingEditor:
    def __init__(self, parent_frame, planet_data):
        self.planet_data = planet_data
        self.frame = ctk.CTkFrame(parent_frame)
        self.frame.pack(fill="both", expand=True)

        self._build_ui()

    # ---------------- UI ----------------
    def _build_ui(self):
        title = ctk.CTkLabel(self.frame, text="Post-Processing Settings", font=("Segoe UI", 18, "bold"))
        title.pack(pady=10)

        pp_data = self.planet_data.get("POST_PROCESSING", {})

        # Exposure
        exp_frame = ctk.CTkFrame(self.frame)
        exp_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(exp_frame, text="Exposure:").pack(side="left", padx=5)
        self.exposure_entry = ctk.CTkEntry(exp_frame, width=100)
        self.exposure_entry.pack(side="left", padx=5)
        self.exposure_entry.insert(0, str(pp_data.get("exposure", "")))

        # Saturation
        sat_frame = ctk.CTkFrame(self.frame)
        sat_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(sat_frame, text="Saturation:").pack(side="left", padx=5)
        self.saturation_entry = ctk.CTkEntry(sat_frame, width=100)
        self.saturation_entry.pack(side="left", padx=5)
        self.saturation_entry.insert(0, str(pp_data.get("saturation", "")))

        # Contrast
        con_frame = ctk.CTkFrame(self.frame)
        con_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(con_frame, text="Contrast:").pack(side="left", padx=5)
        self.contrast_entry = ctk.CTkEntry(con_frame, width=100)
        self.contrast_entry.pack(side="left", padx=5)
        self.contrast_entry.insert(0, str(pp_data.get("contrast", "")))

    # ---------------- DATA EXPORT ----------------
    def get_data(self):
        """
        If the user leaves EVERYTHING empty → DO NOT include POST_PROCESSING.
        """

        exposure = self.exposure_entry.get().strip()
        saturation = self.saturation_entry.get().strip()
        contrast = self.contrast_entry.get().strip()

        # Check if ALL fields are empty
        if exposure == "" and saturation == "" and contrast == "":
            return {}  # <-- remove POST_PROCESSING entirely

        # Build normally
        pp_data = {}

        if exposure != "":
            pp_data["exposure"] = float(exposure)

        if saturation != "":
            pp_data["saturation"] = float(saturation)

        if contrast != "":
            pp_data["contrast"] = float(contrast)

        # If somehow all became empty anyway → remove
        if not pp_data:
            return {}

        return {"POST_PROCESSING": pp_data}
