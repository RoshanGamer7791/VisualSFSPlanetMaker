import tkinter as tk
from tkinter import ttk
import numpy as np
import json


class HeightmapGUI:
    def __init__(self, parent, planet_data, canvas_width=800, canvas_height=400):
        self.parent = parent
        self.planet_data = planet_data

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Heightmap data (200 points by default)
        self.points = np.zeros(200)

        # Main frame for this tab
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Heightmap Editor")

        # Make frame expand fully
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)

        # ---------------------------
        # CANVAS (stretches properly)
        # ---------------------------
        self.canvas = tk.Canvas(
            self.frame,
            bg="white",
            width=self.canvas_width,
            height=self.canvas_height
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Bind drawing
        self.canvas.bind("<B1-Motion>", self.draw_height)
        self.canvas.bind("<Button-1>", self.draw_height)

        # ---------------------------
        # BUTTONS (bottom row)
        # ---------------------------
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=1, column=0, pady=5)

        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Export Heightmap", command=self.export_heightmap).pack(side="left", padx=5)

        # Draw initial empty profile
        self.redraw()

    # ---------------------------------------------------
    # DRAWING
    # ---------------------------------------------------
    def draw_height(self, event):
        """Draw a point based on mouse position."""
        x = max(0, min(self.canvas_width - 1, event.x))
        y = max(0, min(self.canvas_height - 1, event.y))

        # Convert to index
        index = int((x / self.canvas_width) * len(self.points))
        height_value = 1.0 - (y / self.canvas_height)  # normalized 0–1

        if 0 <= index < len(self.points):
            self.points[index] = height_value

        self.redraw()

    def clear(self):
        self.points = np.zeros(len(self.points))
        self.redraw()

    # ---------------------------------------------------
    # DRAW PROFILE
    # ---------------------------------------------------
    def redraw(self):
        self.canvas.delete("all")

        for i in range(len(self.points) - 1):
            x1 = (i / len(self.points)) * self.canvas_width
            y1 = (1.0 - self.points[i]) * self.canvas_height

            x2 = ((i + 1) / len(self.points)) * self.canvas_width
            y2 = (1.0 - self.points[i + 1]) * self.canvas_height

            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    # ---------------------------------------------------
    # EXPORT AS heightmap.txt USING JSON FORMAT
    # ---------------------------------------------------
    def export_heightmap(self):
        heightmap_data = {
            "points": [float(v) for v in self.points]
        }

        with open("heightmap.txt", "w") as f:
            f.write(json.dumps(heightmap_data, indent=4))

        print("Saved heightmap.txt")
