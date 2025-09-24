"""
A smart patcher to update specific, marked sections of the game code.
This version can dynamically add new markers to any file and updates
its own configuration from an external JSON file.
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import re
import os
import json

# ==============================================================================
# The Configuration Manager
# ==============================================================================
CONFIG_FILE = "markers.json"
DEFAULT_MARKERS = [
    # main.py
    {'keyword': '# START:MAIN_IMPORTS', 'file': 'main.py', 'marker': 'MAIN_IMPORTS'},
    {'keyword': '# START:MAIN_GAME_CLASS', 'file': 'main.py', 'marker': 'MAIN_GAME_CLASS'},
    {'keyword': '# START:GAME_INIT', 'file': 'main.py', 'marker': 'GAME_INIT'},
    {'keyword': '# START:GAME_RUN_LOOP', 'file': 'main.py', 'marker': 'GAME_RUN_LOOP'},
    {'keyword': '# START:MAIN_ENTRY_POINT', 'file': 'main.py', 'marker': 'MAIN_ENTRY_POINT'},
    # engine.py
    {'keyword': '# START:ENGINE_IMPORTS', 'file': 'engine.py', 'marker': 'ENGINE_IMPORTS'},
    {'keyword': '# START:ENGINE_CLASS_HEADER', 'file': 'engine.py', 'marker': 'ENGINE_CLASS_HEADER'},
    {'keyword': '# START:ENGINE_INIT', 'file': 'engine.py', 'marker': 'ENGINE_INIT'},
    {'keyword': '# START:ENGINE_RENDER', 'file': 'engine.py', 'marker': 'ENGINE_RENDER'},
    {'keyword': '# START:ENGINE_RENDER_HISTORY', 'file': 'engine.py', 'marker': 'ENGINE_RENDER_HISTORY'},
    {'keyword': '# START:ENGINE_DRAW_TEXT', 'file': 'engine.py', 'marker': 'ENGINE_DRAW_TEXT'},
    {'keyword': '# START:ENGINE_UPDATE_DISPLAY', 'file': 'engine.py', 'marker': 'ENGINE_UPDATE_DISPLAY'},
    {'keyword': '# START:ENGINE_TICK', 'file': 'engine.py', 'marker': 'ENGINE_TICK'},
    # player.py
    {'keyword': '# START:PLAYER_IMPORTS', 'file': 'player.py', 'marker': 'PLAYER_IMPORTS'},
    {'keyword': '# START:PLAYER_CLASS_HEADER', 'file': 'player.py', 'marker': 'PLAYER_CLASS_HEADER'},
    {'keyword': '# START:PLAYER_INIT', 'file': 'player.py', 'marker': 'PLAYER_INIT'},
    {'keyword': '# START:PLAYER_GENERATE_SPRITE', 'file': 'player.py', 'marker': 'PLAYER_GENERATE_SPRITE'},
    {'keyword': '# START:PLAYER_UPDATE', 'file': 'player.py', 'marker': 'PLAYER_UPDATE'},
    {'keyword': '# START:PLAYER_HANDLE_INPUT', 'file': 'player.py', 'marker': 'PLAYER_HANDLE_INPUT'},
    # creature.py
    {'keyword': '# START:CREATURE_IMPORTS', 'file': 'creature.py', 'marker': 'CREATURE_IMPORTS'},
    {'keyword': '# START:CREATURE_CLASS_HEADER', 'file': 'creature.py', 'marker': 'CREATURE_CLASS_HEADER'},
    {'keyword': '# START:CREATURE_INIT', 'file': 'creature.py', 'marker': 'CREATURE_INIT'},
    # config.py
    {'keyword': '# START:CONFIG_SETTINGS', 'file': 'config.py', 'marker': 'CONFIG_SETTINGS'},
    {'keyword': '# START:CONFIG_COLORS', 'file': 'config.py', 'marker': 'CONFIG_COLORS'},
    # assets.py
    {'keyword': '# START:ASSETS_PIXEL_ART', 'file': 'assets.py', 'marker': 'ASSETS_PIXEL_ART'},
]

class MarkerManager:
    def __init__(self):
        self.markers = []
        self.load_markers()

    def load_markers(self):
        if not os.path.exists(CONFIG_FILE):
            self.markers = DEFAULT_MARKERS
            self.save_markers()
        else:
            with open(CONFIG_FILE, 'r') as f:
                self.markers = json.load(f)

    def save_markers(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.markers, f, indent=4)

    def add_marker(self, new_marker):
        self.markers.append(new_marker)
        self.save_markers()

    def find_target(self, code):
        for item in reversed(self.markers):
            if item['keyword'] in code:
                return item['file'], item['marker']
        return None, None

# ==============================================================================
# The Application Logic
# ==============================================================================
class App:
    def __init__(self, root):
        self.marker_manager = MarkerManager()
        self.setup_gui(root)

    def apply_patch(self, file_path, marker_name, new_code):
        # ... (Rest of this function remains the same as before)
        start_marker = f"# START:{marker_name}"
        end_marker = f"# END:{marker_name}"

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return f"ERROR: File not found: {file_path}."

        match = re.search(fr'([ \t]*)({re.escape(start_marker)})', content)
        if not match:
            return f"WARNING: Marker '{marker_name}' not found in {file_path}. Cannot apply patch."
            
        indentation = match.group(1)
        new_code_lines = new_code.strip().split('\n')
        indented_new_code = '\n'.join(indentation + line for line in new_code_lines)

        pattern = re.compile(fr"({re.escape(start_marker)}\n)(.*?)(\n[ \t]*{re.escape(end_marker)})", re.DOTALL)
        
        def repl(m):
            return m.group(1) + indented_new_code + m.group(3)

        new_content, num_subs = pattern.subn(repl, content, count=1)

        if num_subs == 0:
            return f"INFO: No changes applied for '{marker_name}'. The marker block might be malformed."
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"SUCCESS: Patched '{marker_name}' in {file_path}."


    def on_update_button_click(self):
        pasted_code = self.update_text_area.get("1.0", tk.END)
        if not pasted_code.strip():
            messagebox.showwarning("Warning", "Update code area is empty.")
            return

        file_to_update, marker_to_update = self.marker_manager.find_target(pasted_code)

        if not file_to_update:
            messagebox.showerror("Error", "Could not automatically determine where this code goes. Is there a marker for it?")
            return

        result = self.apply_patch(file_to_update, marker_to_update, pasted_code)
        messagebox.showinfo("Update Result", result)

    def on_inject_button_click(self):
        file_path = self.file_entry.get().strip()
        marker_name = self.marker_entry.get().strip().upper()
        code_to_wrap = self.inject_text_area.get("1.0", tk.END).strip()

        if not all([file_path, marker_name, code_to_wrap]):
            messagebox.showwarning("Warning", "All fields for injecting a new marker are required.")
            return
        
        # --- Inject the marker into the target file ---
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
        
        if code_to_wrap not in content:
            messagebox.showerror("Error", "The 'Code to Wrap' was not found in the specified file. Please copy it exactly.")
            return

        start_marker = f"# START:{marker_name}"
        end_marker = f"# END:{marker_name}"
        
        # Find indentation of the first line of the code to wrap
        first_line = code_to_wrap.split('\n')[0]
        match = re.search(fr'^([ \t]*)({re.escape(first_line)})', content, re.MULTILINE)
        indentation = match.group(1) if match else ""

        wrapped_code = f"{indentation}{start_marker}\n{code_to_wrap}\n{indentation}{end_marker}"
        new_content = content.replace(code_to_wrap, wrapped_code)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # --- Update the marker configuration ---
        # Auto-detect a keyword from the code
        new_keyword = start_marker
        
        new_marker_config = {'keyword': new_keyword, 'file': file_path, 'marker': marker_name}
        self.marker_manager.add_marker(new_marker_config)
        
        messagebox.showinfo("Success", f"Successfully injected marker '{marker_name}' into {file_path} and updated configuration.")


    def setup_gui(self, root):
        root.title("Smart Game Patcher (v4 - Self-Improving)")
        root.geometry("800x700")
        root.configure(bg='#2E2E2E')
        
        notebook = ttk.Notebook(root)
        notebook.pack(pady=10, padx=10, expand=True, fill='both')

        # --- Update Tab ---
        update_frame = tk.Frame(notebook, bg='#2E2E2E', padx=10, pady=10)
        notebook.add(update_frame, text='Update Code')
        
        tk.Label(update_frame, text="Paste code block to update an existing section:", fg='white', bg='#2E2E2E').pack(anchor='w')
        self.update_text_area = scrolledtext.ScrolledText(update_frame, wrap=tk.WORD, height=10, bg='#1E1E1E', fg='#D4D4D4', insertbackground='white')
        self.update_text_area.pack(fill='both', expand=True, pady=5)
        tk.Button(update_frame, text="Apply Update", command=self.on_update_button_click, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold')).pack(fill='x', ipady=5)

        # --- Inject Tab ---
        inject_frame = tk.Frame(notebook, bg='#2E2E2E', padx=10, pady=10)
        notebook.add(inject_frame, text='Add New Marker')

        tk.Label(inject_frame, text="Target File (e.g., player.py):", fg='white', bg='#2E2E2E').pack(anchor='w')
        self.file_entry = tk.Entry(inject_frame, bg='#3C3C3C', fg='white', insertbackground='white')
        self.file_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(inject_frame, text="New Marker Name (e.g., PLAYER_ANIMATION):", fg='white', bg='#2E2E2E').pack(anchor='w')
        self.marker_entry = tk.Entry(inject_frame, bg='#3C3C3C', fg='white', insertbackground='white')
        self.marker_entry.pack(fill='x', pady=(0, 10))
        
        tk.Label(inject_frame, text="Exact Code to Wrap:", fg='white', bg='#2E2E2E').pack(anchor='w')
        self.inject_text_area = scrolledtext.ScrolledText(inject_frame, wrap=tk.WORD, height=10, bg='#1E1E1E', fg='#D4D4D4', insertbackground='white')
        self.inject_text_area.pack(fill='both', expand=True, pady=5)
        tk.Button(inject_frame, text="Inject New Marker", command=self.on_inject_button_click, bg='#007ACC', fg='white', font=('Arial', 12, 'bold')).pack(fill='x', ipady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

