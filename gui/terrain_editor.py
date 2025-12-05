import json
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

PLANETS_DIR = "planets"
os.makedirs(PLANETS_DIR, exist_ok=True)

class TerrainEditor:
    """TerrainEditor - edits the entire TERRAIN_DATA block expected by SFS exporter.

    Usage:
        editor = TerrainEditor(parent_frame, planet_data_dict)
        parent_frame should be a container (frame or notebook tab)
        planet_data_dict should be the current planet JSON-like dict (may be empty)

    Methods:
        save()       -- Writes UI values back into self.planet_data
        get_data()   -- Returns the exact TERRAIN_DATA structure expected by exporter
    """

    def __init__(self, parent, planet_data=None):
        self.parent = parent
        self.planet_data = planet_data or {}

        # Frame for tab
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True)

        # Internal state holders
        self.formula_list = []            # list of strings (terrain formula lines for Normal)
        self.texture_formula_list = []    # optional list of texture formula lines
        self.flat_zones = []              # list of dicts {height, angle, width, transition}

        # UI variables (created in build_ui)
        self._create_ui_vars()
        self.build_ui()

    def _create_ui_vars(self):
        # Create variable placeholders so get_data can always read them
        self.planetTexture = ctk.StringVar()
        self.planetTextureCutout = ctk.DoubleVar()

        self.surfaceTexture_A = ctk.StringVar()
        self.surfaceTextureSize_A_x = ctk.DoubleVar()
        self.surfaceTextureSize_A_y = ctk.DoubleVar()

        self.surfaceTexture_B = ctk.StringVar()
        self.surfaceTextureSize_B_x = ctk.DoubleVar()
        self.surfaceTextureSize_B_y = ctk.DoubleVar()

        self.terrainTexture_C = ctk.StringVar()
        self.terrainTextureSize_C_x = ctk.DoubleVar()
        self.terrainTextureSize_C_y = ctk.DoubleVar()

        self.surfaceLayerSize = ctk.DoubleVar()
        self.minFade = ctk.DoubleVar()
        self.maxFade = ctk.DoubleVar()
        self.shadowIntensity = ctk.DoubleVar()
        self.shadowHeight = ctk.DoubleVar()

        self.verticeSize = ctk.DoubleVar()
        self.collider_var = ctk.BooleanVar()

    def build_ui(self):
        # Populate from planet_data defaults when available
        terrain = self.planet_data.get("TERRAIN_DATA", {})
        tex = terrain.get("TERRAIN_TEXTURE_DATA", {})

        # Fill variables with defaults or values
        self.planetTexture.set(tex.get("planetTexture", "Earth"))
        self.planetTextureCutout.set(tex.get("planetTextureCutout", 1.0))

        self.surfaceTexture_A.set(tex.get("surfaceTexture_A", "Blured"))
        sza = tex.get("surfaceTextureSize_A", {"x": 20.0, "y": 8.0})
        self.surfaceTextureSize_A_x.set(sza.get("x", 20.0))
        self.surfaceTextureSize_A_y.set(sza.get("y", 8.0))

        self.surfaceTexture_B.set(tex.get("surfaceTexture_B", "None"))
        szb = tex.get("surfaceTextureSize_B", {"x": -1.0, "y": -1.0})
        self.surfaceTextureSize_B_x.set(szb.get("x", -1.0))
        self.surfaceTextureSize_B_y.set(szb.get("y", -1.0))

        self.terrainTexture_C.set(tex.get("terrainTexture_C", "Blured"))
        tzc = tex.get("terrainTextureSize_C", {"x": 100.0, "y": 30.0})
        self.terrainTextureSize_C_x.set(tzc.get("x", 100.0))
        self.terrainTextureSize_C_y.set(tzc.get("y", 30.0))

        self.surfaceLayerSize.set(tex.get("surfaceLayerSize", 40.0))
        self.minFade.set(tex.get("minFade", 0.0))
        self.maxFade.set(tex.get("maxFade", 1.0))
        self.shadowIntensity.set(tex.get("shadowIntensity", 6.0))
        self.shadowHeight.set(tex.get("shadowHeight", 15.0))

        self.verticeSize.set(terrain.get("verticeSize", 4.0))
        self.collider_var.set(terrain.get("collider", True))

        self.flat_zones = terrain.get("flatZones", [])[:]

        tf = terrain.get("terrainFormulaDifficulties", {})
        normal_formula = tf.get("Normal", [])
        self.formula_list = normal_formula[:] if normal_formula else []

        self.texture_formula_list = terrain.get("textureFormula", [])[:]

        # Build the UI layout
        # Top section: textures
        top = ctk.CTkFrame(self.frame)
        top.pack(fill="x", padx=8, pady=6)

        ctk.CTkLabel(top, text="Planet Texture").grid(row=0, column=0, sticky="w", padx=4, pady=2)
        ctk.CTkEntry(top, textvariable=self.planetTexture).grid(row=0, column=1, sticky="ew", padx=4)
        ctk.CTkLabel(top, text="Planet Texture Cutout").grid(row=0, column=2, sticky="w", padx=4)
        ctk.CTkEntry(top, textvariable=self.planetTextureCutout).grid(row=0, column=3, sticky="ew", padx=4)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(3, weight=1)

        # Surface A
        ctk.CTkLabel(self.frame, text="Surface Texture A").pack(anchor="w", padx=8, pady=(8,2))
        f_a = ctk.CTkFrame(self.frame)
        f_a.pack(fill="x", padx=8)
        ctk.CTkEntry(f_a, textvariable=self.surfaceTexture_A).grid(row=0, column=0, sticky="ew", padx=4, pady=2)
        ctk.CTkLabel(f_a, text="Size X").grid(row=0, column=1, padx=4)
        ctk.CTkEntry(f_a, textvariable=self.surfaceTextureSize_A_x, width=80).grid(row=0, column=2, padx=4)
        ctk.CTkLabel(f_a, text="Size Y").grid(row=0, column=3, padx=4)
        ctk.CTkEntry(f_a, textvariable=self.surfaceTextureSize_A_y, width=80).grid(row=0, column=4, padx=4)
        f_a.columnconfigure(0, weight=1)

        # Surface B
        ctk.CTkLabel(self.frame, text="Surface Texture B").pack(anchor="w", padx=8, pady=(8,2))
        f_b = ctk.CTkFrame(self.frame)
        f_b.pack(fill="x", padx=8)
        ctk.CTkEntry(f_b, textvariable=self.surfaceTexture_B).grid(row=0, column=0, sticky="ew", padx=4, pady=2)
        ctk.CTkLabel(f_b, text="Size X").grid(row=0, column=1, padx=4)
        ctk.CTkEntry(f_b, textvariable=self.surfaceTextureSize_B_x, width=80).grid(row=0, column=2, padx=4)
        ctk.CTkLabel(f_b, text="Size Y").grid(row=0, column=3, padx=4)
        ctk.CTkEntry(f_b, textvariable=self.surfaceTextureSize_B_y, width=80).grid(row=0, column=4, padx=4)
        f_b.columnconfigure(0, weight=1)

        # Terrain C
        ctk.CTkLabel(self.frame, text="Terrain Texture C").pack(anchor="w", padx=8, pady=(8,2))
        f_c = ctk.CTkFrame(self.frame)
        f_c.pack(fill="x", padx=8)
        ctk.CTkEntry(f_c, textvariable=self.terrainTexture_C).grid(row=0, column=0, sticky="ew", padx=4, pady=2)
        ctk.CTkLabel(f_c, text="Size X").grid(row=0, column=1, padx=4)
        ctk.CTkEntry(f_c, textvariable=self.terrainTextureSize_C_x, width=80).grid(row=0, column=2, padx=4)
        ctk.CTkLabel(f_c, text="Size Y").grid(row=0, column=3, padx=4)
        ctk.CTkEntry(f_c, textvariable=self.terrainTextureSize_C_y, width=80).grid(row=0, column=4, padx=4)
        f_c.columnconfigure(0, weight=1)

        # Surface layer and shading
        shade = ctk.CTkFrame(self.frame)
        shade.pack(fill="x", padx=8, pady=6)
        ctk.CTkLabel(shade, text="Surface Layer Size").grid(row=0, column=0, sticky="w")
        ctk.CTkEntry(shade, textvariable=self.surfaceLayerSize, width=100).grid(row=0, column=1, padx=6)
        ctk.CTkLabel(shade, text="Min Fade").grid(row=0, column=2, padx=6)
        ctk.CTkEntry(shade, textvariable=self.minFade, width=80).grid(row=0, column=3, padx=6)
        ctk.CTkLabel(shade, text="Max Fade").grid(row=0, column=4, padx=6)
        ctk.CTkEntry(shade, textvariable=self.maxFade, width=80).grid(row=0, column=5, padx=6)
        ctk.CTkLabel(shade, text="Shadow Intensity").grid(row=1, column=0, sticky="w", pady=(6,0))
        ctk.CTkEntry(shade, textvariable=self.shadowIntensity, width=100).grid(row=1, column=1, padx=6, pady=(6,0))
        ctk.CTkLabel(shade, text="Shadow Height").grid(row=1, column=2, padx=6, pady=(6,0))
        ctk.CTkEntry(shade, textvariable=self.shadowHeight, width=80).grid(row=1, column=3, padx=6, pady=(6,0))

        # Collider and vertice size
        collider_row = ctk.CTkFrame(self.frame)
        collider_row.pack(fill="x", padx=8, pady=6)
        ctk.CTkLabel(collider_row, text="Vertice Size").grid(row=0, column=0, sticky="w")
        ctk.CTkEntry(collider_row, textvariable=self.verticeSize, width=120).grid(row=0, column=1, padx=6)
        ctk.CTkCheckBox(collider_row, text="Collider Enabled", variable=self.collider_var).grid(row=0, column=2, padx=12)

        # Flat zones list
        fz_frame = ctk.CTkFrame(self.frame)
        fz_frame.pack(fill="both", padx=8, pady=6, expand=False)
        ctk.CTkLabel(fz_frame, text="Flat Zones (height, angle, width, transition)").pack(anchor="w")
        self.flatzones_container = ctk.CTkFrame(fz_frame)
        self.flatzones_container.pack(fill="x")
        for z in self.flat_zones:
            self._add_flat_zone_ui(z)

        ctk.CTkButton(fz_frame, text="Add Flat Zone", command=lambda: self._add_flat_zone_ui()).pack(pady=6)

        # Terrain formula textarea
        formula_frame = ctk.CTkFrame(self.frame)
        formula_frame.pack(fill="both", padx=8, pady=6, expand=True)
        ctk.CTkLabel(formula_frame, text="Terrain Formula (Normal)").pack(anchor="w")
        self.formula_text = ctk.CTkTextbox(formula_frame, height=160)
        self.formula_text.pack(fill="both", expand=True)
        if self.formula_list:
            self.formula_text.insert("0.0", "\n".join(self.formula_list))

        # Texture formula (optional)
        ctk.CTkLabel(formula_frame, text="Texture Formula (optional)").pack(anchor="w", pady=(6,0))
        self.texture_formula_text = ctk.CTkTextbox(formula_frame, height=80)
        self.texture_formula_text.pack(fill="both", expand=False)
        if self.texture_formula_list:
            self.texture_formula_text.insert("0.0", "\n".join(self.texture_formula_list))

        # Save button
        bottom = ctk.CTkFrame(self.frame)
        bottom.pack(fill="x", padx=8, pady=8)
        ctk.CTkButton(bottom, text="Save to planet data", command=self.save).pack(side="right")

    def _add_flat_zone_ui(self, data=None):
        data = data or {"height": 18.0, "angle": 1.5707, "width": 900.0, "transition": 200.0}
        row = ctk.CTkFrame(self.flatzones_container)
        row.pack(fill="x", pady=2)

        h = ctk.DoubleVar(value=data.get("height", 0.0))
        a = ctk.DoubleVar(value=data.get("angle", 0.0))
        w = ctk.DoubleVar(value=data.get("width", 0.0))
        t = ctk.DoubleVar(value=data.get("transition", 0.0))

        ctk.CTkEntry(row, textvariable=h, width=12).pack(side="left", padx=4)
        ctk.CTkEntry(row, textvariable=a, width=12).pack(side="left", padx=4)
        ctk.CTkEntry(row, textvariable=w, width=12).pack(side="left", padx=4)
        ctk.CTkEntry(row, textvariable=t, width=12).pack(side="left", padx=4)
        ctk.CTkButton(row, text="Remove", command=lambda: self._remove_flat_zone(row)).pack(side="right", padx=6)

        self.flat_zones.append({"height_var": h, "angle_var": a, "width_var": w, "transition_var": t, "frame": row})

    def _remove_flat_zone(self, frame):
        # remove from ui and internal list
        for e in list(self.flat_zones):
            if e.get("frame") == frame:
                e["frame"].destroy()
                self.flat_zones.remove(e)
                return

    def save(self):
        # Push all values into self.planet_data under TERRAIN_DATA
        terrain = self.planet_data.setdefault("TERRAIN_DATA", {})
        tex = terrain.setdefault("TERRAIN_TEXTURE_DATA", {})

        tex["planetTexture"] = self.planetTexture.get()
        tex["planetTextureCutout"] = float(self.planetTextureCutout.get())

        tex["surfaceTexture_A"] = self.surfaceTexture_A.get()
        tex["surfaceTextureSize_A"] = {"x": float(self.surfaceTextureSize_A_x.get()), "y": float(self.surfaceTextureSize_A_y.get())}

        tex["surfaceTexture_B"] = self.surfaceTexture_B.get()
        tex["surfaceTextureSize_B"] = {"x": float(self.surfaceTextureSize_B_x.get()), "y": float(self.surfaceTextureSize_B_y.get())}

        tex["terrainTexture_C"] = self.terrainTexture_C.get()
        tex["terrainTextureSize_C"] = {"x": float(self.terrainTextureSize_C_x.get()), "y": float(self.terrainTextureSize_C_y.get())}

        tex["surfaceLayerSize"] = float(self.surfaceLayerSize.get())
        tex["minFade"] = float(self.minFade.get())
        tex["maxFade"] = float(self.maxFade.get())
        tex["shadowIntensity"] = float(self.shadowIntensity.get())
        tex["shadowHeight"] = float(self.shadowHeight.get())

        terrain["verticeSize"] = float(self.verticeSize.get())
        terrain["collider"] = bool(self.collider_var.get())

        # Flat zones: convert UI vars into plain dicts
        flat_list = []
        for e in self.flat_zones:
            # if stored as dict with vars
            if "height_var" in e:
                flat_list.append({
                    "height": float(e["height_var"].get()),
                    "angle": float(e["angle_var"].get()),
                    "width": float(e["width_var"].get()),
                    "transition": float(e["transition_var"].get())
                })
            else:
                # legacy raw dict
                flat_list.append({
                    "height": float(e.get("height", 0)),
                    "angle": float(e.get("angle", 0)),
                    "width": float(e.get("width", 0)),
                    "transition": float(e.get("transition", 0))
                })

        terrain["flatZones"] = flat_list

        # Terrain formula
        formula_raw = self.formula_text.get("0.0", "end").strip()
        if formula_raw:
            terrain["terrainFormulaDifficulties"] = {"Normal": [line for line in formula_raw.splitlines() if line.strip() != ""]}
        else:
            terrain["terrainFormulaDifficulties"] = {}

        # Texture formula
        t_raw = self.texture_formula_text.get("0.0", "end").strip()
        terrain["textureFormula"] = [l for l in t_raw.splitlines() if l.strip()] if t_raw else []

        # write back to planet_data
        self.planet_data["TERRAIN_DATA"] = terrain
        messagebox.showinfo("Saved", "Terrain settings saved into planet data (in-memory).")

    def get_data(self):
        """Return the exact TERRAIN_DATA structure expected by SFS exporter"""
        tex = {
            "planetTexture": self.planetTexture.get(),
            "planetTextureCutout": float(self.planetTextureCutout.get()),
            "surfaceTexture_A": self.surfaceTexture_A.get(),
            "surfaceTextureSize_A": {
                "x": float(self.surfaceTextureSize_A_x.get()),
                "y": float(self.surfaceTextureSize_A_y.get())
            },
            "surfaceTexture_B": self.surfaceTexture_B.get(),
            "surfaceTextureSize_B": {
                "x": float(self.surfaceTextureSize_B_x.get()),
                "y": float(self.surfaceTextureSize_B_y.get())
            },
            "terrainTexture_C": self.terrainTexture_C.get(),
            "terrainTextureSize_C": {
                "x": float(self.terrainTextureSize_C_x.get()),
                "y": float(self.terrainTextureSize_C_y.get())
            },
            "surfaceLayerSize": float(self.surfaceLayerSize.get()),
            "minFade": float(self.minFade.get()),
            "maxFade": float(self.maxFade.get()),
            "shadowIntensity": float(self.shadowIntensity.get()),
            "shadowHeight": float(self.shadowHeight.get())
        }

        # Flat zones
        flat_list = []
        for e in self.flat_zones:
            if "height_var" in e:
                flat_list.append({
                    "height": float(e["height_var"].get()),
                    "angle": float(e["angle_var"].get()),
                    "width": float(e["width_var"].get()),
                    "transition": float(e["transition_var"].get())
                })
            else:
                flat_list.append({
                    "height": float(e.get("height", 0)),
                    "angle": float(e.get("angle", 0)),
                    "width": float(e.get("width", 0)),
                    "transition": float(e.get("transition", 0))
                })

        # Terrain formula
        formula_raw = self.formula_text.get("0.0", "end").strip()
        if formula_raw:
            terrain_formula = {"Normal": [line for line in formula_raw.splitlines() if line.strip() != ""]}
        else:
            terrain_formula = {}

        texture_formula_raw = self.texture_formula_text.get("0.0", "end").strip()
        texture_formula = [l for l in texture_formula_raw.splitlines() if l.strip()] if texture_formula_raw else []

        terrain = {
            "TERRAIN_TEXTURE_DATA": tex,
            "terrainFormulaDifficulties": terrain_formula,
            "textureFormula": texture_formula,
            "verticeSize": float(self.verticeSize.get()),
            "collider": bool(self.collider_var.get()),
            "flatZones": flat_list
        }

        return {"TERRAIN_DATA": terrain}
