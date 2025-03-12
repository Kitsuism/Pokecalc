# MIT License
# 
# Copyright (c) 2025 Skye Riverthrone AKA Kitsuism/Kitsuism913
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# You must give appropriate credit to the original author(s), provide a link to the license, and indicate if changes were made.
# You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import tkinter as tk
import os
from tkinter import ttk

# --- App Icon and Title ---
def set_icon(app):
    """ Set the window icon if icon.ico exists, otherwise skip. """
    icon_path = "icon.ico"
    if os.path.exists(icon_path):
        app.iconbitmap(icon_path)

# --- All Calculation Logic ---
def calculate_matchups():
    def format_effectiveness(effectiveness, label):
        sorted_effects = sorted(effectiveness, key=lambda x: -x[1])
        lines = []
        current_line = []
        for t, m in sorted_effects:
            current_line.append(f"{t} (x{m})")
            if len(current_line) == 4:
                lines.append(", ".join(current_line))
                current_line = []
        if current_line:
            lines.append(", ".join(current_line))
        return "\n".join(lines)

    my_types = [my_type1.get(), my_type2.get()]
    enemy_types = [enemy_type1.get(), enemy_type2.get()]

    def get_effectiveness(types):
        weakness = {}
        resistance = {}
        for t in types:
            if t in type_chart:
                for w in type_chart[t]["weakness"]:
                    weakness[w] = weakness.get(w, 1) * 2
                for r in type_chart[t]["resistance"]:
                    resistance[r] = resistance.get(r, 1) * 0.5
                for i in type_chart[t]["immune"]:
                    resistance[i] = 0

        # Neutralizing contradictory effects:
        # Remove resistance from weakness or vice versa if they neutralize
        for w in list(weakness.keys()):
            if w in resistance:
                del weakness[w]
                del resistance[w]

        return list(weakness.items()), list(resistance.items())

    enemy_weakness, enemy_resistance = get_effectiveness(enemy_types)
    my_weakness, my_resistance = get_effectiveness(my_types)

    result_text.set(f"Enemy Weaknesses:\n{format_effectiveness(enemy_weakness, 'Weaknesses')}\n\n"
                    f"Enemy Resistances:\n{format_effectiveness(enemy_resistance, 'Resistances')}\n\n"
                    f"Your Weaknesses:\n{format_effectiveness(my_weakness, 'Weaknesses')}\n\n"
                    f"Your Resistances:\n{format_effectiveness(my_resistance, 'Resistances')}")

# --- The About Button ---
def open_about_window():
    about_window = tk.Toplevel(app)
    
    # Get position of the main window
    main_x = app.winfo_x()
    main_y = app.winfo_y()
    
    # Center the About window relative to the main window
    about_window_width = 320
    about_window_height = 470
    about_window.geometry(f'{about_window_width}x{about_window_height}+{main_x + 50}+{main_y + 50}')
    about_window.title("About")

    # Create a frame to hold the text labels
    about_frame = tk.Frame(about_window)
    about_frame.pack(pady=20)

    # Custom text with "POKECALC" in bold and large
    title_label = tk.Label(about_frame, text="POKÉCALC", font=("Arial", 20, "bold"))
    title_label.pack()

    version_label = tk.Label(about_frame, text="v1.0", font=("Arial", 10))
    version_label.pack()

    description_label = tk.Label(about_frame, text="A program to quickly and reliably find\ntype strengths and weaknesses.\n\nAll code by kitsuism\n\nIcon by Ramy Wafaa on icon-icons.com\n\n\nPokéCalc is a fan-made application created \nfor educational purposes.\nIt is not affiliated with or endorsed by Nintendo\nGame Freak, or The Pokémon Company.\nAll trademarks related to Pokémon are \nthe property of their respective owners.\n\n\nBy using this program you agree:\n\nHonestly just don't steal it lol", font=("Arial", 10), justify="center")
    description_label.pack()

    # Close button
    close_btn = tk.Button(about_window, text="Close", command=about_window.destroy)
    close_btn.pack(pady=0)

# --- Window Size ---
app = tk.Tk()
app.title("PokéCalc")
app.geometry("400x650")

# Center the main window on the screen
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 400
window_height = 650
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
app.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# --- Type Chart ---
type_chart = {
    "None": {"weakness": [], "resistance": [], "immune": []},
    "Fire": {"weakness": ["Water", "Rock", "Ground"], "resistance": ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"], "immune": []},
    "Water": {"weakness": ["Electric", "Grass"], "resistance": ["Fire", "Water", "Ice", "Steel"], "immune": []},
    "Grass": {"weakness": ["Fire", "Ice", "Flying", "Poison", "Bug"], "resistance": ["Water", "Electric", "Grass", "Ground"], "immune": []},
    "Electric": {"weakness": ["Ground"], "resistance": ["Electric", "Flying", "Steel"], "immune": []},
    "Ice": {"weakness": ["Fire", "Fighting", "Rock", "Steel"], "resistance": ["Ice"], "immune": []},
    "Fighting": {"weakness": ["Flying", "Psychic", "Fairy"], "resistance": ["Bug", "Rock", "Dark"], "immune": []},
    "Poison": {"weakness": ["Ground", "Psychic"], "resistance": ["Grass", "Fighting", "Poison", "Bug", "Fairy"], "immune": []},
    "Ground": {"weakness": ["Water", "Ice", "Grass"], "resistance": ["Poison", "Rock"], "immune": ["Electric"]},
    "Flying": {"weakness": ["Electric", "Ice", "Rock"], "resistance": ["Fighting", "Bug", "Grass"], "immune": ["Ground"]},
    "Psychic": {"weakness": ["Bug", "Ghost", "Dark"], "resistance": ["Fighting", "Psychic"], "immune": []},
    "Bug": {"weakness": ["Fire", "Flying", "Rock"], "resistance": ["Grass", "Fighting", "Ground"], "immune": []},
    "Rock": {"weakness": ["Water", "Grass", "Fighting", "Ground", "Steel"], "resistance": ["Normal", "Fire", "Poison", "Flying"], "immune": []},
    "Normal": {"weakness": ["Fighting"], "resistance": [], "immune": ["Ghost"]},
    "Ghost": {"weakness": ["Ghost", "Dark"], "resistance": ["Poison", "Bug"], "immune": ["Normal", "Fighting"]},
    "Dragon": {"weakness": ["Ice", "Dragon", "Fairy"], "resistance": ["Fire", "Water", "Electric", "Grass"], "immune": []},
    "Dark": {"weakness": ["Fighting", "Bug", "Fairy"], "resistance": ["Ghost", "Dark"], "immune": ["Psychic"]},
    "Steel": {"weakness": ["Fire", "Fighting", "Ground"], "resistance": ["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"], "immune": ["Poison"]},
    "Fairy": {"weakness": ["Poison", "Steel"], "resistance": ["Fighting", "Bug", "Dark"], "immune": ["Dragon"]}    
}

# --- All UI Code for the Main Window ---
# Set the icon (will skip if icon.ico is missing)
set_icon(app)

# Add instructions to be displayed on launch
title_label = tk.Label(app, text="POKÉCALC", font=("Arial", 24, "bold"))
title_label.pack(pady=(20, 10))

# Place About button at the top-left, overlapping the title padding
about_btn = tk.Button(app, text="About", command=open_about_window)
about_btn.place(x=10, y=10)

subtitle_label = tk.Label(app, text="A matchup calculator")
subtitle_label.pack()

result_text = tk.StringVar()
# Instructions will show up here initially
result_text.set("Select types for your Pokémon and for your opponent.\nThe program will calculate their weaknesses and resistances\nbased on type interactions.")

result_label = tk.Label(app, textvariable=result_text, width=80, height=20)
result_label.pack(pady=2)

types_frame = tk.Frame(app)
types_frame.pack(pady=2)

my_label = tk.Label(types_frame, text="Your Types")
my_label.grid(row=0, column=0, padx=5)
my_type1 = ttk.Combobox(types_frame, values=list(type_chart.keys()))
my_type1.grid(row=1, column=0, pady=5)
my_type2 = ttk.Combobox(types_frame, values=list(type_chart.keys()))
my_type2.grid(row=2, column=0, pady=5)

enemy_label = tk.Label(types_frame, text="Opponent's Types")
enemy_label.grid(row=0, column=1, padx=5)
enemy_type1 = ttk.Combobox(types_frame, values=list(type_chart.keys()))
enemy_type1.grid(row=1, column=1, pady=5)
enemy_type2 = ttk.Combobox(types_frame, values=list(type_chart.keys()))
enemy_type2.grid(row=2, column=1, pady=5)

calculate_btn = tk.Button(app, text="Calculate", command=calculate_matchups)
calculate_btn.pack(pady=5)

# --- Run the Application ---
app.mainloop()
