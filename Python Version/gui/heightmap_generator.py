# Version/gui/heightmap_generator.py url=https://github.com/RoshanGamer7791/VisualSFSPlanetMaker/blob/a99c7d2a4bf2cb6abbc9dfa1fdaefb2ea0f44f80/Python%20Version/gui/heightmap_generator.py
import tkinter as tk
import customtkinter as ctk
import numpy as np
import json
from tkinter import filedialog, messagebox

class HeightmapGUI:
    """
    Heightmap editor tab.

    Changes made:
    - Use a CTkFrame compatible with the other editor tabs (do NOT call parent.add inside this class;
      main.py is expected to add the tab).
    - Canvas resizes with the frame and redraws appropriately.
    - Export now opens a Save dialog so user can choose where to save (keeps same JSON-in-.txt format).
    - Added a 'Save to Project' button that stores the heightmap into the provided planet_data dict
      under the key "HEIGHTMAP" (as {"points":[...]}) so other parts of the app can access it.
    """

    def __init__(self, parent, planet_data=None, canvas_width=800, canvas_height=400, points_count=200):
        self.parent = parent
        self.planet_data = planet_data if isinstance(planet_data, dict) else {}

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Heightmap data (points_count points by default)
        self.points = np.zeros(points_count, dtype=float)

        # Main frame for this tab (don't call parent.add here; main will add the frame to its notebook)
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        # Allow the canvas to expand
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # ---------------------------
        # CANVAS (stretches properly)
        # ---------------------------
        self.canvas = tk.Canvas(
            self.frame,
            bg="white",
            width=self.canvas_width,
            height=self.canvas_height,
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Bind drawing and resizing
        self.canvas.bind("<B1-Motion>", self.draw_height)
        self.canvas.bind("<Button-1>", self.draw_height)
        self.canvas.bind("<Configure>", self.on_resize)

        # ---------------------------
        # BUTTONS (bottom row)
        # ---------------------------
        btn_frame = ctk.CTkFrame(self.frame)
        btn_frame.grid(row=1, column=0, pady=8)

        clear_btn = ctk.CTkButton(btn_frame, text="Clear", command=self.clear)
        clear_btn.pack(side="left", padx=6)

        export_btn = ctk.CTkButton(btn_frame, text="Export Heightmap", command=self.export_heightmap)
        export_btn.pack(side="left", padx=6)

        save_proj_btn = ctk.CTkButton(btn_frame, text="Save to Project", command=self.save_to_project)
        save_proj_btn.pack(side="left", padx=6)

        # Draw initial empty profile
        self.redraw()

    # ---------------------------------------------------
    # EVENT: canvas resized
    # ---------------------------------------------------
    def on_resize(self, event):
        # Update stored canvas size and redraw to fit new dimensions
        self.canvas_width = max(1, event.width)
        self.canvas_height = max(1, event.height)
        self.redraw()

    # ---------------------------------------------------
    # DRAWING
    # ---------------------------------------------------
    def draw_height(self, event):
        """Draw a point based on mouse position."""
        # Translate mouse coordinates to local canvas coordinates (already local for tk events)
        x = max(0, min(self.canvas_width - 1, event.x))
        y = max(0, min(self.canvas_height - 1, event.y))

        # Convert to index
        index = int((x / max(1, self.canvas_width)) * len(self.points))
        height_value = 1.0 - (y / max(1, self.canvas_height))  # normalized 0–1

        if 0 <= index < len(self.points):
            self.points[index] = float(height_value)

        self.redraw()

    def clear(self):
        self.points.fill(0.0)
        self.redraw()

    # ---------------------------------------------------
    # DRAW PROFILE
    # ---------------------------------------------------
    def redraw(self):
        self.canvas.delete("all")

        w = max(1, self.canvas_width)
        h = max(1, self.canvas_height)

        if len(self.points) < 2:
            return

        for i in range(len(self.points) - 1):
            x1 = (i / (len(self.points) - 1)) * w
            y1 = (1.0 - float(self.points[i])) * h

            x2 = ((i + 1) / (len(self.points) - 1)) * w
            y2 = (1.0 - float(self.points[i + 1])) * h

            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

        # Optionally draw a bounding rectangle
        self.canvas.create_rectangle(0, 0, w - 1, h - 1, outline="#cccccc")

    # ---------------------------------------------------
    # EXPORT AS heightmap.txt USING JSON FORMAT (with Save dialog)
    # ---------------------------------------------------
    def export_heightmap(self):
        heightmap_data = {
            "points": [float(v) for v in self.points]
        }

        file_path = filedialog.asksaveasfilename(
            title="Export Heightmap",
            defaultextension=".txt",
            filetypes=[("Heightmap Text", "*.txt"), ("JSON", "*.json"), ("All files", "*.*")],
            initialfile="heightmap.txt"
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(heightmap_data, f, indent=2)
            messagebox.showinfo("Export Complete", f"Heightmap exported to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export heightmap:\n{e}")

    # ---------------------------------------------------
    # Save the heightmap data into the in-memory project dict
    # ---------------------------------------------------
    def save_to_project(self):
        self.planet_data["HEIGHTMAP"] = {"points": [float(v) for v in self.points]}
        messagebox.showinfo("Saved", "Heightmap saved to project data (in-memory).")
