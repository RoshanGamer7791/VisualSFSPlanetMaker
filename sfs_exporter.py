import os
import json

class SFSExporter:
    def __init__(self, planet_data):
        self.data = planet_data

    def export_planet(self, save_path):
        """
        Writes JSON planet data into a .txt file.
        Planet name = filename (without extension).
        """

        # Planet name is based on file name ONLY
        planet_name = os.path.splitext(os.path.basename(save_path))[0]

        # Build JSON dictionary
        planet_json = self.build_planet_json(planet_name)

        # Save JSON text directly into the txt file
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(planet_json, f, indent=4)

        return save_path

    def build_planet_json(self, planet_name):
        """Returns the JSON-ready dictionary"""

        json_data = {
            "name": planet_name,
            "radius": self.data.get("radius", 600000),
            "color": self.data.get("color", "#ffffff"),
            "heightmap": self.data.get("heightmap", None),
            "biomes": self.data.get("biomes", []),
            "atmosphere": self.data.get("atmosphere", {}),
            "orbit": self.data.get("orbit", {}),
            "landmarks": self.data.get("landmarks", []),
            "post_processing": self.data.get("post_processing", {})
        }

        # Remove None values
        clean = {k: v for k, v in json_data.items() if v is not None}
        return clean
