# gui/post_properties.py
import tkinter as tk
from tkinter import ttk, messagebox

class PostProcessingEditor(ttk.Frame):
    def __init__(self, master, planet_data):
        super().__init__(master)
        self.master = master
        self.planet_data = planet_data
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Post Processing Keys").grid(row=0, column=0, sticky="w", pady=5)

        self.keys_listbox = tk.Listbox(self, width=80, height=10)
        self.keys_listbox.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        self.refresh_keys()

        ttk.Button(self, text="Add Key", command=self.add_key).grid(row=2, column=0, pady=5)
        ttk.Button(self, text="Remove Key", command=self.remove_key).grid(row=2, column=1, pady=5)

    def refresh_keys(self):
        self.keys_listbox.delete(0, tk.END)
        keys = self.planet_data.get("POST_PROCESSING", {}).get("keys", [])
        for i, key in enumerate(keys):
            display = f"Key {i}: height={key.get('height',0)}, shadow={key.get('shadowIntensity',0)}"
            self.keys_listbox.insert(tk.END, display)

    def add_key(self):
        new_key = {
            "height": 0.0,
            "shadowIntensity": 1.0,
            "starIntensity": 0.0,
            "hueShift": 0.0,
            "saturation": 1.0,
            "contrast": 1.0,
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        }
        self.planet_data.setdefault("POST_PROCESSING", {}).setdefault("keys", []).append(new_key)
        self.refresh_keys()
        messagebox.showinfo("Added", "New post-processing key added.")

    def remove_key(self):
        selected = self.keys_listbox.curselection()
        if selected:
            index = selected[0]
            keys = self.planet_data.get("POST_PROCESSING", {}).get("keys", [])
            if 0 <= index < len(keys):
                keys.pop(index)
                self.refresh_keys()
                messagebox.showinfo("Removed", f"Key {index} removed.")
        else:
            messagebox.showwarning("Select Key", "Please select a key to remove.")
