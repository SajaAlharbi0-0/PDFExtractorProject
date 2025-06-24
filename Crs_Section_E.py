import docx
import json
import os

# ==== CONFIG ====
docx_path = r"C:\Users\mahaf\Downloads\crs sp2.w.docx"  # ← عدّل المسار إذا تغير الملف
output_json_path = "C:\\Users\\mahaf\\Downloads\\section_e_output.json"

def extract_section_e_from_docx(file_path):
    doc = docx.Document(file_path)

    refs = {
        "References and Learning Resources": {
            "Essential References": [],
            "Supportive References": [],
            "Electronic Materials": [],
            "Other Learning Materials": []
        },
        "Required Facilities and Equipment": {
            "Facilities": "",
            "Technology equipment": "",
            "Other equipment": ""
        }
    }

    current_ref = None
    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) != 2:
                continue
            key, value = cells
            key_lower = key.lower()

            # References
            if "essential references" in key_lower:
                refs["References and Learning Resources"]["Essential References"].append(value)
                current_ref = "Essential References"
            elif "supportive references" in key_lower:
                refs["References and Learning Resources"]["Supportive References"].append(value)
                current_ref = "Supportive References"
            elif "electronic materials" in key_lower:
                refs["References and Learning Resources"]["Electronic Materials"].append(value)
                current_ref = "Electronic Materials"
            elif "other learning materials" in key_lower:
                refs["References and Learning Resources"]["Other Learning Materials"].append(value)
                current_ref = "Other Learning Materials"

            # Equipment
            elif "facilities" in key_lower:
                refs["Required Facilities and Equipment"]["Facilities"] = value
            elif "technology equipment" in key_lower:
                refs["Required Facilities and Equipment"]["Technology equipment"] = value
            elif "other equipment" in key_lower:
                refs["Required Facilities and Equipment"]["Other equipment"] = value

    return refs

# ==== RUN ====
section_e_data = extract_section_e_from_docx(docx_path)

with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(section_e_data, f, ensure_ascii=False, indent=2)

print("✅ Section E extracted and saved to:", output_json_path)
