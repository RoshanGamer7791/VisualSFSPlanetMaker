# gui/orbit_editor.py
import math
import tkinter as tk
import customtkinter as ctk

class OrbitEditor:
    """
    OrbitEditor (CTk) - fixed canvas 500x500.

    Usage:
      tab = OrbitEditor(parent, planet_data)
      parent_tab_control.add(tab.frame, text="Orbit")

    Public API:
      - .frame : CTkFrame container (for adding to notebook)
      - .get_data() -> dict with ORBIT_DATA exactly matching required SFS structure
      - .save() updates internal planet_data dict from UI (optional)
    """

    def __init__(self, parent, planet_data=None):
        self.parent = parent
        self.planet_data = planet_data or {}
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True)

        # default values (match SFS defaults you provided)
        orbit = (self.planet_data.get("ORBIT_DATA") or {})
        self.parent_name = orbit.get("parent", "Sun")
        self.semiMajorAxis = float(orbit.get("semiMajorAxis", 7480000000.0))  # meters
        self.eccentricity = float(orbit.get("eccentricity", 0.0))
        self.arg_peri = float(orbit.get("argumentOfPeriapsis", 0.0))  # degrees
        self.direction = int(orbit.get("direction", 1))  # 1 or -1
        self.multiplierSOI = float(orbit.get("multiplierSOI", 2.5))

        # UI constants
        self.canvas_size = 500
        self.center = (self.canvas_size // 2, self.canvas_size // 2)
        # default mapping: pixels -> meters (meters per pixel)
        # Pick a default so typical SMA (1e9..1e10) fits comfortably
        self.meters_per_pixel = 4e7  # 40 million meters per pixel (tweakable by user)

        # State
        self.dragging = False
        self.dot_pos = (0, 0)  # pixel coords on canvas

        self.build_ui()
        self.redraw()

    def build_ui(self):
        left = ctk.CTkFrame(self.frame)
        left.pack(side="left", fill="both", expand=False, padx=8, pady=8)

        right = ctk.CTkFrame(self.frame)
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        # Canvas for orbit preview (tk.Canvas embedded)
        self.canvas = tk.Canvas(right, width=self.canvas_size, height=self.canvas_size, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=False)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)            # Windows
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)             # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)             # Linux scroll down

        # Left-side controls
        ctk.CTkLabel(left, text="Parent (type):").grid(row=0, column=0, sticky="w", padx=6, pady=(4,2))
        self.parent_entry = ctk.CTkEntry(left, width=200)
        self.parent_entry.grid(row=1, column=0, padx=6, pady=(0,8))
        self.parent_entry.insert(0, str(self.parent_name))

        # SMA (meters) entry (user can type to set)
        ctk.CTkLabel(left, text="Semi-major axis (m):").grid(row=2, column=0, sticky="w", padx=6, pady=(4,2))
        self.sma_var = ctk.StringVar(value=str(self.semiMajorAxis))
        self.sma_entry = ctk.CTkEntry(left, textvariable=self.sma_var)
        self.sma_entry.grid(row=3, column=0, padx=6, pady=(0,8))
        self.sma_entry.bind("<Return>", lambda e: self.on_sma_entry())

        # Meters per pixel
        ctk.CTkLabel(left, text="Meters per pixel:").grid(row=4, column=0, sticky="w", padx=6, pady=(4,2))
        self.scale_var = ctk.StringVar(value=str(self.meters_per_pixel))
        self.scale_entry = ctk.CTkEntry(left, textvariable=self.scale_var)
        self.scale_entry.grid(row=5, column=0, padx=6, pady=(0,8))
        self.scale_entry.bind("<Return>", lambda e: self.on_scale_entry())

        # Eccentricity slider
        ctk.CTkLabel(left, text="Eccentricity:").grid(row=6, column=0, sticky="w", padx=6, pady=(4,2))
        self.ecc_slider = ctk.CTkSlider(left, from_=0.0, to=0.99, number_of_steps=99, command=self.on_ecc_change)
        self.ecc_slider.set(self.eccentricity)
        self.ecc_slider.grid(row=7, column=0, padx=6, pady=(0,8))

        # Argument of Periapsis slider
        ctk.CTkLabel(left, text="Argument of Periapsis (deg):").grid(row=8, column=0, sticky="w", padx=6, pady=(4,2))
        self.arg_slider = ctk.CTkSlider(left, from_=0.0, to=360.0, command=self.on_arg_change)
        self.arg_slider.set(self.arg_peri)
        self.arg_slider.grid(row=9, column=0, padx=6, pady=(0,8))

        # Direction switch
        ctk.CTkLabel(left, text="Direction:").grid(row=10, column=0, sticky="w", padx=6, pady=(4,2))
        self.dir_var = ctk.StringVar(value="Prograde" if self.direction==1 else "Retrograde")
        self.dir_switch = ctk.CTkOptionMenu(left, values=["Prograde","Retrograde"], command=self.on_direction_change)
        self.dir_switch.set("Prograde" if self.direction==1 else "Retrograde")
        self.dir_switch.grid(row=11, column=0, padx=6, pady=(0,8))

        # Buttons: snap view, reset
        btn_frame = ctk.CTkFrame(left)
        btn_frame.grid(row=12, column=0, padx=6, pady=(6,2), sticky="ew")
        ctk.CTkButton(btn_frame, text="Center & Fit", command=self.center_and_fit).pack(side="left", padx=4, pady=4)
        ctk.CTkButton(btn_frame, text="Reset", command=self.reset_defaults).pack(side="right", padx=4, pady=4)

        # Info label
        self.info_label = ctk.CTkLabel(left, text="Drag the white dot to set SMA.\nMouse wheel zooms (meters per pixel).", wraplength=200, justify="left")
        self.info_label.grid(row=13, column=0, padx=6, pady=(8,2))

        # initial dot position
        self.update_dot_from_sma()

    # --------------------
    # UI callbacks & helpers
    # --------------------
    def on_sma_entry(self):
        try:
            v = float(self.sma_var.get())
            if v <= 0:
                return
            self.semiMajorAxis = v
            self.update_dot_from_sma()
            self.redraw()
        except Exception:
            pass

    def on_scale_entry(self):
        try:
            v = float(self.scale_var.get())
            if v <= 0:
                return
            self.meters_per_pixel = v
            self.update_dot_from_sma()
            self.redraw()
        except Exception:
            pass

    def on_ecc_change(self, val):
        try:
            self.eccentricity = float(val)
            self.redraw()
        except Exception:
            pass

    def on_arg_change(self, val):
        try:
            self.arg_peri = float(val)
            self.update_dot_from_sma()  # keep dot aligned to argument
            self.redraw()
        except Exception:
            pass

    def on_direction_change(self, val):
        self.direction = 1 if val == "Prograde" else -1
        self.redraw()

    def center_and_fit(self):
        # Ensure the current SMA is visible by adjusting meters_per_pixel automatically
        # Fit such that semiMajorAxis maps to ~200 pixels
        if self.semiMajorAxis > 0:
            self.meters_per_pixel = max(1.0, self.semiMajorAxis / 200.0)
            self.scale_var.set(str(self.meters_per_pixel))
            self.update_dot_from_sma()
            self.redraw()

    def reset_defaults(self):
        self.semiMajorAxis = 7480000000.0
        self.eccentricity = 0.0
        self.arg_peri = 0.0
        self.direction = 1
        self.meters_per_pixel = 4e7
        self.sma_var.set(str(self.semiMajorAxis))
        self.scale_var.set(str(self.meters_per_pixel))
        self.arg_slider.set(self.arg_peri)
        self.ecc_slider.set(self.eccentricity)
        self.dir_switch.set("Prograde")
        self.update_dot_from_sma()
        self.redraw()

    def on_canvas_click(self, event):
        # Start dragging if clicked near the dot; else treat as a move to set SMA
        x, y = event.x, event.y
        dx = x - self.dot_pos[0]
        dy = y - self.dot_pos[1]
        dist = math.hypot(dx, dy)
        if dist <= 10:
            self.dragging = True
        else:
            # place dot / set SMA directly
            self.set_dot_and_sma_from_pixel(x, y)
            self.redraw()

    def on_canvas_drag(self, event):
        if self.dragging:
            self.set_dot_and_sma_from_pixel(event.x, event.y)
            self.redraw()

    def on_canvas_release(self, event):
        self.dragging = False

    def on_mouse_wheel(self, event):
        # Zoom in/out by changing meters_per_pixel
        # MouseWheel on Windows uses event.delta; Linux uses Button-4/5
        delta = 0
        if hasattr(event, "delta"):
            delta = event.delta
        elif event.num == 4:
            delta = 120
        elif event.num == 5:
            delta = -120

        factor = 0.9 if delta > 0 else 1.1
        # smaller meters_per_pixel => zoom in (show more detail)
        self.meters_per_pixel = max(1.0, self.meters_per_pixel * factor)
        self.scale_var.set(str(self.meters_per_pixel))
        self.update_dot_from_sma()
        self.redraw()

    # --------------------
    # Dot / SMA mapping
    # --------------------
    def set_dot_and_sma_from_pixel(self, px, py):
        # compute pixel distance from center (focus at center)
        cx, cy = self.center
        dx = px - cx
        dy = py - cy
        pixel_dist = math.hypot(dx, dy)
        # Convert pixel distance to meters via meters_per_pixel
        sma = max(1.0, pixel_dist * self.meters_per_pixel)
        self.semiMajorAxis = sma
        self.sma_var.set(str(self.semiMajorAxis))
        # store dot position clipped inside canvas
        self.dot_pos = (max(0, min(self.canvas_size, px)), max(0, min(self.canvas_size, py)))

    def update_dot_from_sma(self):
        # Place dot along the +x axis rotated by argument of periapsis (so it's easy to see)
        # compute pixel distance corresponding to SMA
        px_dist = self.semiMajorAxis / max(1.0, self.meters_per_pixel)
        # angle = arg_peri degrees
        ang = math.radians(self.arg_peri)
        cx, cy = self.center
        x = cx + px_dist * math.cos(ang) * self.direction
        y = cy + px_dist * math.sin(ang) * self.direction
        # clamp inside canvas
        x = max(0, min(self.canvas_size, x))
        y = max(0, min(self.canvas_size, y))
        self.dot_pos = (x, y)
        self.sma_var.set(str(self.semiMajorAxis))

    # --------------------
    # Drawing
    # --------------------
    def redraw(self):
        self.canvas.delete("all")
        cx, cy = self.center

        # draw parent body at center
        parent_radius = 6
        self.canvas.create_oval(cx-parent_radius, cy-parent_radius, cx+parent_radius, cy+parent_radius, fill="#ffd700", outline="")

        # compute ellipse points (focus at center)
        a = max(1.0, self.semiMajorAxis)
        e = max(0.0, min(0.99, self.eccentricity))
        b = a * math.sqrt(max(0.0, 1 - e*e))
        c = a * e  # focal distance

        # Parametric ellipse with focus at (0,0): x = a*cos(t) - c, y = b*sin(t)
        pts = []
        steps = 180
        ang_rot = math.radians(self.arg_peri)  # rotate ellipse by argument of periapsis
        for i in range(steps+1):
            t = 2*math.pi * (i/steps)
            x_orb = a * math.cos(t) - c
            y_orb = b * math.sin(t)
            # rotate
            xr = x_orb * math.cos(ang_rot) - y_orb * math.sin(ang_rot)
            yr = x_orb * math.sin(ang_rot) + y_orb * math.cos(ang_rot)
            # map meters -> pixels
            px = cx + (xr / max(1.0, self.meters_per_pixel))
            py = cy + (yr / max(1.0, self.meters_per_pixel))
            pts.append((px, py))

        # draw ellipse as polyline
        for i in range(len(pts)-1):
            x1, y1 = pts[i]
            x2, y2 = pts[i+1]
            self.canvas.create_line(x1, y1, x2, y2, fill="white")

        # draw periapsis and apoapsis points (position relative to center)
        # periapsis at true anomaly = 0 in our param -> position x = a - c rotated
        peri_x = a - c
        peri_y = 0
        # rotate
        prx = peri_x * math.cos(ang_rot) - peri_y * math.sin(ang_rot)
        pry = peri_x * math.sin(ang_rot) + peri_y * math.cos(ang_rot)
        per_px = cx + prx / max(1.0, self.meters_per_pixel)
        per_py = cy + pry / max(1.0, self.meters_per_pixel)
        self.canvas.create_oval(per_px-4, per_py-4, per_px+4, per_py+4, fill="red", outline="")

        # apoapsis at true anomaly = pi
        apo_x = -a - c
        apo_y = 0
        arx = apo_x * math.cos(ang_rot) - apo_y * math.sin(ang_rot)
        ary = apo_x * math.sin(ang_rot) + apo_y * math.cos(ang_rot)
        apo_px = cx + arx / max(1.0, self.meters_per_pixel)
        apo_py = cy + ary / max(1.0, self.meters_per_pixel)
        self.canvas.create_oval(apo_px-4, apo_py-4, apo_px+4, apo_py+4, fill="blue", outline="")

        # draw the draggable dot
        dot_x, dot_y = self.dot_pos
        self.canvas.create_oval(dot_x-6, dot_y-6, dot_x+6, dot_y+6, fill="white", outline="")

        # info overlay
        info_text = f"SMA: {int(self.semiMajorAxis)} m\nEcc: {self.eccentricity:.3f}\nArg: {self.arg_peri:.1f}°\nDir: {'1' if self.direction==1 else '-1'}"
        self.canvas.create_text(8, 8, anchor="nw", fill="white", text=info_text, font=("TkDefaultFont", 10))

    # --------------------
    # Data export / integration helpers
    # --------------------
    def save(self):
        """Push UI values into self.planet_data dictionary (optional helper)."""
        orbit = self.planet_data.setdefault("ORBIT_DATA", {})
        orbit["parent"] = self.parent_entry.get()
        orbit["semiMajorAxis"] = float(self.semiMajorAxis)
        orbit["smaDifficultyScale"] = orbit.get("smaDifficultyScale", {})
        orbit["eccentricity"] = float(self.eccentricity)
        orbit["argumentOfPeriapsis"] = float(self.arg_peri)
        orbit["direction"] = int(self.direction)
        orbit["multiplierSOI"] = float(self.multiplierSOI)
        orbit["soiDifficultyScale"] = orbit.get("soiDifficultyScale", {})

    def get_data(self):
        """Return the exact ORBIT_DATA structure expected by SFS exporter"""
        return {
            "ORBIT_DATA": {
                "parent": self.parent_entry.get() or "Sun",
                "semiMajorAxis": float(self.semiMajorAxis),
                "smaDifficultyScale": {},
                "eccentricity": float(self.eccentricity),
                "argumentOfPeriapsis": float(self.arg_peri),
                "direction": int(self.direction),
                "multiplierSOI": float(self.multiplierSOI),
                "soiDifficultyScale": {}
            }
        }

# Standalone test (optional)
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")
    editor = OrbitEditor(root, {})
    editor.frame.pack(fill="both", expand=True)
    root.mainloop()
