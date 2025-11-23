import customtkinter as ctk

class TerrainEditor:
    def __init__(self, parent, planet_data):
        self.parent = parent
        self.planet_data = planet_data
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        terrain = self.planet_data.get("TERRAIN_DATA", {})
        tex = terrain.get("TERRAIN_TEXTURE_DATA", {})

        # Planet Texture
        self.planetTexture = ctk.StringVar(value=tex.get("planetTexture", "None"))
        ctk.CTkLabel(self.frame, text="Planet Texture").pack(padx=5, pady=2, anchor="w")
        ctk.CTkEntry(self.frame, textvariable=self.planetTexture).pack(fill="x", padx=5, pady=2)

        # Planet Texture Cutout
        self.planetTextureCutout = ctk.DoubleVar(value=tex.get("planetTextureCutout", 1.0))
        ctk.CTkLabel(self.frame, text="Planet Texture Cutout").pack(padx=5, pady=2, anchor="w")
        ctk.CTkEntry(self.frame, textvariable=self.planetTextureCutout).pack(fill="x", padx=5, pady=2)

        # Surface Textures
        for surf in ["surfaceTexture_A", "surfaceTexture_B", "terrainTexture_C"]:
            var = ctk.StringVar(value=tex.get(surf, "None"))
            ctk.CTkLabel(self.frame, text=f"{surf}").pack(padx=5, pady=2, anchor="w")
            ctk.CTkEntry(self.frame, textvariable=var).pack(fill="x", padx=5, pady=2)
            setattr(self, surf, var)

        # Surface Texture Sizes
        for size in ["surfaceTextureSize_A", "surfaceTextureSize_B", "terrainTextureSize_C"]:
            size_data = tex.get(size, {"x": -1, "y": -1})
            x_var = ctk.DoubleVar(value=size_data.get("x", -1))
            y_var = ctk.DoubleVar(value=size_data.get("y", -1))
            ctk.CTkLabel(self.frame, text=f"{size} X").pack(padx=5, pady=2, anchor="w")
            ctk.CTkEntry(self.frame, textvariable=x_var).pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(self.frame, text=f"{size} Y").pack(padx=5, pady=2, anchor="w")
            ctk.CTkEntry(self.frame, textvariable=y_var).pack(fill="x", padx=5, pady=2)
            setattr(self, f"{size}_x", x_var)
            setattr(self, f"{size}_y", y_var)

        # Surface Layer Size
        self.surfaceLayerSize = ctk.DoubleVar(value=tex.get("surfaceLayerSize", 40.0))
        ctk.CTkLabel(self.frame, text="Surface Layer Size").pack(padx=5, pady=2, anchor="w")
        ctk.CTkEntry(self.frame, textvariable=self.surfaceLayerSize).pack(fill="x", padx=5, pady=2)

        # Collider
        self.collider = ctk.BooleanVar(value=tex.get("collider", True))
        ctk.CTkCheckBox(self.frame, text="Collider Enabled", variable=self.collider).pack(padx=5, pady=5)

        # Flat Zones
        self.flatZones = terrain.get("flatZones", [])
        self.flatZone_entries = []
        for i, zone in enumerate(self.flatZones):
            f_frame = ctk.CTkFrame(self.frame)
            f_frame.pack(fill="x", padx=5, pady=2)
            h_var = ctk.DoubleVar(value=zone.get("height", 0))
            angle_var = ctk.DoubleVar(value=zone.get("angle", 0))
            width_var = ctk.DoubleVar(value=zone.get("width", 0))
            transition_var = ctk.DoubleVar(value=zone.get("transition", 0))

            for label, var in [("Height", h_var), ("Angle", angle_var), ("Width", width_var), ("Transition", transition_var)]:
                ctk.CTkLabel(f_frame, text=label).pack(anchor="w", padx=5)
                ctk.CTkEntry(f_frame, textvariable=var).pack(fill="x", padx=5, pady=2)

            self.flatZone_entries.append({
                "height": h_var,
                "angle": angle_var,
                "width": width_var,
                "transition": transition_var
            })

        # Terrain Formula
        self.terrainFormula = terrain.get("terrainFormulaDifficulties", {})
        ctk.CTkLabel(self.frame, text="Terrain Formula (Normal)").pack(padx=5, pady=2, anchor="w")
        self.terrainFormulaText = ctk.CTkTextbox(self.frame, height=100)
        normal_formula = "\n".join(self.terrainFormula.get("Normal", []))
        self.terrainFormulaText.insert("0.0", normal_formula)
        self.terrainFormulaText.pack(fill="both", padx=5, pady=2)

    def save(self):
        terrain = self.planet_data.setdefault("TERRAIN_DATA", {})
        tex = terrain.setdefault("TERRAIN_TEXTURE_DATA", {})

        tex["planetTexture"] = self.planetTexture.get()
        tex["planetTextureCutout"] = self.planetTextureCutout.get()
        tex["surfaceTexture_A"] = self.surfaceTexture_A.get()
        tex["surfaceTexture_B"] = self.surfaceTexture_B.get()
        tex["terrainTexture_C"] = self.terrainTexture_C.get()

        for size in ["surfaceTextureSize_A", "surfaceTextureSize_B", "terrainTextureSize_C"]:
            tex[size] = {
                "x": getattr(self, f"{size}_x").get(),
                "y": getattr(self, f"{size}_y").get()
            }

        tex["surfaceLayerSize"] = self.surfaceLayerSize.get()
        tex["collider"] = self.collider.get()

        # Flat Zones
        terrain["flatZones"] = []
        for f in self.flatZone_entries:
            terrain["flatZones"].append({
                "height": f["height"].get(),
                "angle": f["angle"].get(),
                "width": f["width"].get(),
                "transition": f["transition"].get()
            })

        # Terrain Formula
        terrain["terrainFormulaDifficulties"] = {
            "Normal": self.terrainFormulaText.get("0.0", "end").strip().split("\n")
        }

    def get_data(self):
        return {
            "TERRAIN_DATA": {
                "TERRAIN_TEXTURE_DATA": {
                    "planetTexture": self.tex_planet.get(),
                    "planetTextureCutout": float(self.cutout.get() or 1.0),
                    "surfaceTexture_A": self.texture_a.get(),
                    "surfaceTextureSize_A": {
                        "x": float(self.tx_a_x.get() or 0),
                        "y": float(self.tx_a_y.get() or 0)
                    },
                    "surfaceTexture_B": self.texture_b.get(),
                    "surfaceTextureSize_B": {
                        "x": float(self.tx_b_x.get() or 0),
                        "y": float(self.tx_b_y.get() or 0)
                    },
                },
                "verticeSize": float(self.vertex.get() or 4.0),
                "collider": True,
                "flatZones": []
            }
        }
