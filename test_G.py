import docx
import json

# ==== CONFIG ====
file_path = r"C:\Users\mahaf\Downloads\crs sp1.w.docx"
output_json_path = r"C:\Users\mahaf\Downloads\section_F_only.json"

def extract_section_f_from_docx(file_path):
    doc = docx.Document(file_path)

    data = {
       "Assessment of Course Quality": [],
        "Specification Approval": {
            "Council/Committee": "",
            "Reference Number": "",
            "Date": ""
        }
    }

    # Look for the table containing the F section
    for table in doc.tables:
        headers = [cell.text.strip().lower() for cell in table.rows[0].cells]
        if any("committee" in cell for cell in first_row) and any("reference" in cell for cell in first_row):
            for row in table.rows[1:]:
                cells = [cell.text.strip() for cell in row.cells]
                if len(cells) >= 3:
                    data["Specification Approval"]["Council/Committee"] = cells[0]
                    data["Specification Approval"]["Reference Number"] = cells[1]
                    data["Specification Approval"]["Date"] = cells[2]
                    break  # found it; stop

    return data

# ==== RUN ====
section_f = extract_section_f_from_docx(file_path)

with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(section_f, f, ensure_ascii=False, indent=2)

print("✅ Section F extracted and saved to:", output_json_path)