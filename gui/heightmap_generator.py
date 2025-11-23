import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class HeightmapGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Heightmap Generator")
        self.canvas_width = 800
        self.canvas_height = 200
        self.points_count = 64  # default number of points
        self.points = [0.5] * self.points_count  # default flat
        self.filename = None

        # Canvas
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<B1-Motion>", self.draw_height)
        self.canvas.bind("<Button-1>", self.draw_height)

        # Buttons
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Button(frame, text="Load", command=self.load_heightmap).pack(side="left", padx=5)
        tk.Button(frame, text="Save", command=self.save_heightmap).pack(side="left", padx=5)
        tk.Button(frame, text="Clear", command=self.clear_heightmap).pack(side="left", padx=5)

        self.draw_canvas()
        self.root.mainloop()

    def draw_canvas(self):
        self.canvas.delete("all")
        step = self.canvas_width / (self.points_count - 1)
        for i in range(self.points_count - 1):
            x1 = i * step
            y1 = self.canvas_height - self.points[i] * self.canvas_height
            x2 = (i + 1) * step
            y2 = self.canvas_height - self.points[i + 1] * self.canvas_height
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)

    def draw_height(self, event):
        step = self.canvas_width / (self.points_count - 1)
        index = int(event.x / step)
        if 0 <= index < self.points_count:
            # Convert canvas y to 0-1 float
            self.points[index] = max(0.0, min(1.0, 1 - event.y / self.canvas_height))
            self.draw_canvas()

    def clear_heightmap(self):
        self.points = [0.5] * self.points_count
        self.draw_canvas()

    def load_heightmap(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    self.points = data.get("points", [0.5]*self.points_count)
                    self.points_count = len(self.points)
                    self.draw_canvas()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load heightmap: {e}")

    def save_heightmap(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                         filetypes=[("Text files", "*.txt")])
        if self.filename:
            try:
                with open(self.filename, "w") as f:
                    json.dump({"points": self.points}, f, indent=4)
                messagebox.showinfo("Saved", f"Heightmap saved to {self.filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save heightmap: {e}")

# Run standalone
if __name__ == "__main__":
    HeightmapGenerator()
