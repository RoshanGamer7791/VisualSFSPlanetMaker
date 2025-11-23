import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class TerrainEditor(ttk.Frame):
    def __init__(self, parent, planet_data):
        super().__init__(parent)
        self.planet_data = planet_data

        ttk.Label(self, text="Terrain Editor", font=("Segoe UI", 14, "bold")).pack(pady=5)

        terrain = self.planet_data["TERRAIN_DATA"]
        tex = terrain["TERRAIN_TEXTURE_DATA"]

        self.formula_frame = ttk.LabelFrame(self, text="Terrain Formula")
        self.formula_frame.pack(fill="x", pady=5)

        ttk.Button(self.formula_frame, text="Edit Terrain Formula", command=self.edit_formula).pack(fill="x", pady=5)

        # Texture Data Section
        self.tex_frame = ttk.LabelFrame(self, text="Texture Settings")
        self.tex_frame.pack(fill="x", pady=5)

        self.planetTexture = self.text_entry("Planet Texture", tex, "planetTexture", self.tex_frame)
        self.planetTextureCutout = self.num_entry("Planet Cutout", tex, "planetTextureCutout", self.tex_frame)

        self.surfaceTexture_A = self.text_entry("Surface Texture A", tex, "surfaceTexture_A", self.tex_frame)
        self.surfaceTextureSize_A_x = self.num_entry("Texture A Size X", tex["surfaceTextureSize_A"], "x", self.tex_frame)
        self.surfaceTextureSize_A_y = self.num_entry("Texture A Size Y", tex["surfaceTextureSize_A"], "y", self.tex_frame)

        self.surfaceTexture_B = self.text_entry("Surface Texture B", tex, "surfaceTexture_B", self.tex_frame)
        self.surfaceTextureSize_B_x = self.num_entry("Texture B Size X", tex["surfaceTextureSize_B"], "x", self.tex_frame)
        self.surfaceTextureSize_B_y = self.num_entry("Texture B Size Y", tex["surfaceTextureSize_B"], "y", self.tex_frame)

        self.terrainTexture_C = self.text_entry("Terrain Texture C", tex, "terrainTexture_C", self.tex_frame)
        self.terrainTextureSize_C_x = self.num_entry("Texture C Size X", tex["terrainTextureSize_C"], "x", self.tex_frame)
        self.terrainTextureSize_C_y = self.num_entry("Texture C Size Y", tex["terrainTextureSize_C"], "y", self.tex_frame)

        self.surfaceLayerSize = self.num_entry("Surface Layer Size", tex, "surfaceLayerSize", self.tex_frame)
        self.minFade = self.num_entry("Min Fade", tex, "minFade", self.tex_frame)
        self.maxFade = self.num_entry("Max Fade", tex, "maxFade", self.tex_frame)
        self.shadowIntensity = self.num_entry("Shadow Intensity", tex, "shadowIntensity", self.tex_frame)
        self.shadowHeight = self.num_entry("Shadow Height", tex, "shadowHeight", self.tex_frame)

        # Vertice & Collider
        self.vert_frame = ttk.LabelFrame(self, text="Mesh Settings")
        self.vert_frame.pack(fill="x", pady=5)

        self.verticeSize = self.num_entry("Vertice Size", terrain, "verticeSize", self.vert_frame)

        self.collider_var = tk.BooleanVar(value=terrain["collider"])
        ttk.Checkbutton(self.vert_frame, text="Enable Collider", variable=self.collider_var,
                        command=self.update_collider).pack(anchor="w")

        # Flat Zones
        self.flat_frame = ttk.LabelFrame(self, text="Flat Zones")
        self.flat_frame.pack(fill="x", pady=5)

        ttk.Button(self.flat_frame, text="Edit Flat Zones", command=self.edit_flat_zones).pack(fill="x", pady=5)

    # ----------------------
    # Entry Factories
    # ----------------------
    def text_entry(self, label, data, key, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="x")
        ttk.Label(frame, text=label).pack(side="left")

        var = tk.StringVar(value=data.get(key, ""))
        entry = ttk.Entry(frame, textvariable=var)
        entry.pack(side="right", fill="x", expand=True)

        def update(*_):
            data[key] = var.get()

        var.trace_add("write", update)
        return var

    def num_entry(self, label, data, key, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="x")
        ttk.Label(frame, text=label).pack(side="left")

        var = tk.DoubleVar(value=data.get(key, 0.0))
        entry = ttk.Entry(frame, textvariable=var)
        entry.pack(side="right", fill="x", expand=True)

        def update(*_):
            try:
                data[key] = float(var.get())
            except:
                pass

        var.trace_add("write", update)
        return var

    def update_collider(self):
        self.planet_data["TERRAIN_DATA"]["collider"] = bool(self.collider_var.get())

    # ----------------------
    # Terrain Formula Editor
    # ----------------------
    def edit_formula(self):
        terrain = self.planet_data["TERRAIN_DATA"]

        win = tk.Toplevel(self)
        win.title("Edit Terrain Formula")

        ttk.Label(win, text="Enter terrainFormula (one rule per line):").pack()

        text = tk.Text(win, width=80, height=20)
        text.pack()

        initial = "\n".join(terrain["textureFormula"])
        text.insert("1.0", initial)

        def save():
            terrain["textureFormula"] = [
                line.strip() for line in text.get("1.0", "end").split("\n") if line.strip()
            ]
            messagebox.showinfo("Saved", "Terrain formula updated.")
            win.destroy()

        ttk.Button(win, text="Save", command=save).pack()

    # ----------------------
    # Flat Zones Editor
    # ----------------------
    def edit_flat_zones(self):
        terrain = self.planet_data["TERRAIN_DATA"]

        win = tk.Toplevel(self)
        win.title("Edit Flat Zones")

        listbox = tk.Listbox(win, width=60)
        listbox.pack()

        for zone in terrain["flatZones"]:
            listbox.insert("end", f"Height {zone['height']} | Angle {zone['angle']} | Width {zone['width']}")

        def add_zone():
            h = simpledialog.askfloat("Height", "Height:")
            a = simpledialog.askfloat("Angle", "Angle:")
            w = simpledialog.askfloat("Width", "Width:")
            t = simpledialog.askfloat("Transition", "Transition:")

            if None in (h, a, w, t):
                return

            new = {"height": h, "angle": a, "width": w, "transition": t}
            terrain["flatZones"].append(new)
            listbox.insert("end", f"Height {h} | Angle {a} | Width {w}")

        def delete_zone():
            index = listbox.curselection()
            if not index:
                return
            idx = index[0]
            terrain["flatZones"].pop(idx)
            listbox.delete(idx)

        ttk.Button(win, text="Add Zone", command=add_zone).pack(fill="x")
        ttk.Button(win, text="Delete Selected", command=delete_zone).pack(fill="x")

