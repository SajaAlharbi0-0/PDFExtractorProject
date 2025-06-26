import json
import tkinter as tk
from tkinter import scrolledtext

# Load JSON
with open("crs_sp2.json") as f:
    data = json.load(f)

sections_b = data["Sections"]["B"]

# Create window
root = tk.Tk()
root.title("Course Learning Outcomes and Assessments")
root.geometry("700x400")

# Add scrollable text widget
text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
text.pack(expand=True, fill='both')

# Populate text
text.insert(tk.END, "📘 Course Learning Outcomes and Assessment Methods:\n\n")

for category, outcomes in sections_b.items():
    if not outcomes:
        continue
    text.insert(tk.END, f"🔹 {category}\n")
    for outcome in outcomes:
        clo = outcome['Course Learning Outcome']
        assess = outcome['Assessment Methods']
        text.insert(tk.END, f"  ➤ Outcome: {clo}\n     Assessed by: {assess}\n\n")

root.mainloop()
