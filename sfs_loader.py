import json
from tkinter import filedialog, messagebox

def choose_and_load_planet():
    """
    Opens a file dialog to select a JSON planet file and returns the loaded data as a Python dict.
    """
    file_path = filedialog.askopenfilename(
        title="Select a planet JSON file",
        filetypes=[("JSON Files", "*.json")]
    )
    if not file_path:
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load planet file:\n{e}")
        return None
