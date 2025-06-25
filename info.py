from docx import Document
import json
from tkinter import filedialog, Tk

# Hide tkinter window and let user select file
Tk().withdraw()
doc_path = filedialog.askopenfilename(title="Select course spec file", filetypes=[("Word", "*.docx")])
if not doc_path:
    print("❌ No file selected.")
    exit()

doc = Document(doc_path)

# Initial course info structure
course_info = {
    "Course Title": "",
    "Course Code": "",
    "Program": "",
    "Department": "",
    "Faculty": "",
    "University": "",
    "Version": "",
    "Last Revision Date": ""
}

# Flexible keywords → label mapping
expected_labels = {
    "course title": "Course Title",
    "title": "Course Title",
    "course code": "Course Code",
    "code": "Course Code",
    "program": "Program",
    "department": "Department",
    "faculty": "Faculty",
    "college": "Faculty",
    "institution": "University",
    "university": "University",
    "version": "Version",
    "last revision date": "Last Revision Date",
    "revision date": "Last Revision Date"
}

already_filled = set()

# Search all tables
for table in doc.tables:
    for row in table.rows:
        cells = row.cells
        if len(cells) == 2:
            label = cells[0].text.strip().lower()
            value = cells[1].text.strip()
            for key, field in expected_labels.items():
                if key in label and field not in already_filled:
                    course_info[field] = value
                    already_filled.add(field)
        elif len(cells) == 1:
            text = cells[0].text.strip()
            if ":" in text:
                label, value = text.split(":", 1)
                label = label.strip().lower()
                value = value.strip()
                for key, field in expected_labels.items():
                    if key in label and field not in already_filled:
                        course_info[field] = value
                        already_filled.add(field)

# Show result
print(json.dumps(course_info, indent=2, ensure_ascii=False))

# Optional: save
with open("course_info_extracted.json", "w", encoding="utf-8") as f:
    json.dump(course_info, f, ensure_ascii=False, indent=2)
