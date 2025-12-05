import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Import editors
from gui.planet_properties import PlanetPropertiesEditor
from gui.post_properties import PostProcessingEditor
from gui.atmo_editor import AtmosphereEditor
from gui.terrain_editor import TerrainEditor
from gui.landmarks_editor import LandmarksEditor
from gui.orbit_editor import OrbitEditor
from gui.heightmap_generator import HeightmapGUI

# Import loader/exporter
from sfs_loader import choose_and_load_planet
from sfs_exporter import SFSExporter


class PlanetMakerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SFS Planet Maker")
        self.geometry("1000x700")

        self.planet_data = {}
        self.file_path = None

        self.create_menu()
        self.create_tabs()

    # ---------------------------------------------
    # MENU
    # ---------------------------------------------
    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_command(label="Load Planet", command=self.load_planet)
        file_menu.add_command(label="Export Planet", command=self.export_planet)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    # ---------------------------------------------
    # TABS
    # ---------------------------------------------
    def create_tabs(self):
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=True, fill="both")

        # Initialize tabs with empty data
        self.planet_properties_tab = PlanetPropertiesEditor(self.tab_control, self.planet_data)
        self.post_properties_tab = PostProcessingEditor(self.tab_control, self.planet_data)
        self.atmo_editor_tab = AtmosphereEditor(self.tab_control, self.planet_data)
        self.terrain_editor_tab = TerrainEditor(self.tab_control, self.planet_data)
        self.landmarks_editor_tab = LandmarksEditor(self.tab_control, self.planet_data)
        self.orbit_editor_tab = OrbitEditor(self.tab_control, self.planet_data)
        self.heightmap_tab = HeightmapGUI(self.tab_control, self.planet_data)

        self.tab_control.add(self.planet_properties_tab.frame, text="Planet Properties")
        self.tab_control.add(self.post_properties_tab.frame, text="Post Properties")
        self.tab_control.add(self.atmo_editor_tab.frame, text="Atmosphere")
        self.tab_control.add(self.terrain_editor_tab.frame, text="Terrain")
        self.tab_control.add(self.landmarks_editor_tab.frame, text="Landmarks")
        self.tab_control.add(self.orbit_editor_tab.frame, text="Orbit")
        self.tab_control.add(self.heightmap_tab.frame, text="Heightmap Generator")

    # ---------------------------------------------
    # LOAD PLANET
    # ---------------------------------------------
    def load_planet(self):
        path = filedialog.askopenfilename(
            title="Select Planet File",
            filetypes=[("SFS Planet Files", "*.txt")]
        )
        if not path:
            return

        self.planet_data = load_planet_file(path)
        self.file_path = path

        # Update all editors
        self.planet_properties_tab.update_data(self.planet_data)
        self.post_properties_tab.update_data(self.planet_data)
        self.atmo_editor_tab.update_data(self.planet_data)
        self.terrain_editor_tab.update_data(self.planet_data)
        self.landmarks_editor_tab.update_data(self.planet_data)
        self.orbit_editor_tab.update_data(self.planet_data)
        self.heightmap_tab.update_data(self.planet_data)

        messagebox.showinfo("Loaded", f"Loaded planet: {os.path.basename(path)}")

    # ---------------------------------------------
    # EXPORT PLANET
    # ---------------------------------------------
    def export_planet(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("SFS Planet File", "*.txt")],
            title="Save Planet File"
        )

        if not save_path:
            return

        # Gather data from all tabs
        planet_data = self.collect_editor_data()

        exporter = SFSExporter(planet_data)
        exporter.export_planet(save_path)

        messagebox.showinfo("Export Complete", f"Planet saved to:\n{save_path}")

    # ---------------------------------------------
    # COLLECT DATA FROM EDITORS
    # ---------------------------------------------
    def collect_editor_data(self):
        data = {}

        data.update(self.planet_properties_tab.get_data())
        data.update(self.post_properties_tab.get_data())
        data.update(self.atmo_editor_tab.get_data())
        data.update(self.orbit_editor_tab.get_data())
        data.update(self.terrain_editor_tab.get_data())
        data.update(self.landmarks_editor_tab.get_data())
        data.update(self.heightmap_tab.get_data())

        return data


if __name__ == "__main__":
    app = PlanetMakerApp()
    app.mainloop()
