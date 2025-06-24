# G.py
import docx
import json

# ==== CONFIG ====
docx_path = "crs sp2 (1).docx"  # Adjust path as needed
output_g_path = "section_g_output.json"

def extract_section_g(file_path):
    doc = docx.Document(file_path)
    section_g = {
        "Council/Committee": "",
        "Reference No.": "",
        "Date": ""
    }

    for table in doc.tables:
        headers = [cell.text.strip().lower() for cell in table.rows[0].cells]

        if any("council" in h or "reference" in h or "date" in h for h in headers):
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                if len(cells) >= 2:
                    key = cells[0].lower()
                    value = cells[1]
                    if "council" in key:
                        section_g["Council/Committee"] = value
                    elif "reference" in key:
                        section_g["Reference No."] = value
                    elif "date" in key:
                        section_g["Date"] = value
            break  # Stop after finding the table

    return section_g

# ==== RUN ====
section_g_data = extract_section_g(docx_path)

with open(output_g_path, "w", encoding="utf-8") as f:
    json.dump({"Specification Approval": section_g_data}, f, ensure_ascii=False, indent=2)

print("✅ Section G saved to:", output_g_path)
