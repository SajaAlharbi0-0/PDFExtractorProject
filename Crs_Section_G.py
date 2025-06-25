import docx
import json

# ==== CONFIG ====
<<<<<<< HEAD
docx_path = r"C:\Users\mahaf\Downloads\crs sp1.w.docx"
output_g_path = r"C:\Users\mahaf\Downloads\section_g_only.json"
=======
docx_path = "crs_spfinal.docx"  # Update as needed
output_json_path = "_G_output.json"
>>>>>>> 9f1e9feccab5b4fdd734f14f751bf176edcd598a

def extract_G(file_path):
    doc = docx.Document(file_path)

    result = {
        "Specification Approval": {
            "Council/Committee": "",
            "Reference No.": "",
            "Date": ""
        }
    }

    for table in doc.tables:
        headers = [cell.text.strip().lower() for cell in table.rows[0].cells]

        # --- Specification Approval Section ---
        if any("council" in h or "reference" in h or "date" in h for h in headers):
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
section_data = extract_G(docx_path)

with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(section_data, f, ensure_ascii=False, indent=2)

print("✅ Specification Approval extracted and saved to:", output_json_path)
