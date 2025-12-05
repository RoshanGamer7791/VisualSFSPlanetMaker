# sfs_exporter.py
import json
import os

class SFSExporter:
    """
    Exports planet data to Spaceflight Simulator (.txt) format.
    """

    def __init__(self):
        pass

    def export_planet(self, filepath: str, planet_data: dict):
        """
        Export a planet to a .txt file in SFS format.

        Args:
            filepath (str): Path to save the .txt file.
            planet_data (dict): Planet data dictionary structured like SFS.
        """

        if not isinstance(filepath, str) or not filepath:
            raise TypeError("filepath must be a string path to save the planet .txt file.")

        if not isinstance(planet_data, dict):
            raise TypeError("planet_data must be a dictionary with the planet information.")

        # Ensure all major keys exist
        default_structure = {
            "version": "1.5",
            "BASE_DATA": {},
            "ATMOSPHERE_PHYSICS_DATA": {},
            "ATMOSPHERE_VISUALS_DATA": {},
            "TERRAIN_DATA": {},
            "POST_PROCESSING": {},
            "ORBIT_DATA": {},
            "ACHIEVEMENT_DATA": {
                "Landed": False,
                "Takeoff": True,
                "Atmosphere": True,
                "Orbit": True,
                "Crash": True
            },
            "LANDMARKS": []
        }

        # Merge provided data with default structure to avoid missing keys
        full_data = {**default_structure, **planet_data}

        # Handle empty terrainFormulaDifficulties
        if "terrainFormulaDifficulties" in full_data.get("TERRAIN_DATA", {}):
            if not full_data["TERRAIN_DATA"]["terrainFormulaDifficulties"]:
                full_data["TERRAIN_DATA"]["terrainFormulaDifficulties"] = {}

        # Handle empty post-processing keys
        if "keys" not in full_data.get("POST_PROCESSING", {}):
            full_data["POST_PROCESSING"]["keys"] = []

        # Handle missing flatZones
        if "flatZones" not in full_data.get("TERRAIN_DATA", {}):
            full_data["TERRAIN_DATA"]["flatZones"] = []

        # Ensure all keys are serializable
        try:
            json_text = json.dumps(full_data, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to serialize planet data: {e}")

        # Create directory if it does not exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_text)

        print(f"Planet exported successfully to: {filepath}")
