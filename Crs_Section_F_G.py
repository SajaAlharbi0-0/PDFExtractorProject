import docx
import json

# ==== CONFIG ====
docx_path = "crs sp2 (1).docx"  # Update as needed
output_json_path = "_Gg_approval_output.json"

def extract_F_and_G(file_path):
    doc = docx.Document(file_path)

    result = {
        "Assessment of Course Quality": [],
        "Specification Approval": {
            "Council/Committee": "",
            "Reference No.": "",
            "Date": ""
        }
    }

    for table in doc.tables:
        headers = [cell.text.strip().lower() for cell in table.rows[0].cells]

        # --- Section G: Assessment of Course Quality ---
        if "assessment areas/issues" in headers and "assessor" in headers and "assessment methods" in headers:
            for row in table.rows[1:]:
                cells = [cell.text.strip() for cell in row.cells]
                if len(cells) >= 3:
                    result["Assessment of Course Quality"].append({
                        "Assessment Area/Issue": cells[0],
                        "Assessor": cells[1],
                        "Assessment Method": cells[2]
                    })

        # --- Specification Approval Section ---
        elif any("council" in h or "reference" in h or "date" in h for h in headers):
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                if len(cells) >= 2:
                    key = cells[0].lower()
                    value = cells[1]
                    if "council" in key:
                        result["Specification Approval"]["Council/Committee"] = value
                    elif "reference" in key:
                        result["Specification Approval"]["Reference No."] = value
                    elif "date" in key:
                        result["Specification Approval"]["Date"] = value

    return result

# ==== RUN ====
section_data = extract_F_and_G(docx_path)

with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(section_data, f, ensure_ascii=False, indent=2)

print("✅ Section G & Specification Approval extracted and saved to:", output_json_path)
