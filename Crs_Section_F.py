import docx
import json

# ==== CONFIG ====
file_path = r"C:\Users\mahaf\Downloads\crs sp1.w.docx"
output_json_path = r"C:\Users\mahaf\Downloads\section_F_only.json"

def extract_section_f_from_docx(file_path):
    doc = docx.Document(file_path)

    section_f_data = {
        "Assessment of Course Quality": []
    }

    # Look for the table containing the F section
    for table in doc.tables:
        headers = [cell.text.strip().lower() for cell in table.rows[0].cells]
        if "assessment areas/issues" in headers and "assessor" in headers and "assessment methods" in headers:
            for row in table.rows[1:]:
                cells = [cell.text.strip() for cell in row.cells]
                if len(cells) >= 3:
                    section_f_data["Assessment of Course Quality"].append({
                        "Area/Issue": cells[0],
                        "Assessor": cells[1],
                        "Method": cells[2]
                    })
            break  # Found the section, no need to check more tables

    return section_f_data

# ==== RUN ====
section_f = extract_section_f_from_docx(file_path)

with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(section_f, f, ensure_ascii=False, indent=2)

print("✅ Section F extracted and saved to:", output_json_path)