import json
import os

PLANETS_FOLDER = os.path.join(os.path.dirname(__file__), "planets")

if not os.path.exists(PLANETS_FOLDER):
    os.makedirs(PLANETS_FOLDER)

def export_planet_to_file(planet_data, planet_name):
    """
    Export planet data to a JSON-formatted .txt file in the planets folder.
    """
    path = os.path.join(PLANETS_FOLDER, f"{planet_name}.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(planet_data, f, indent=4)
        return path
    except Exception as e:
        raise IOError(f"Failed to export planet: {e}")
