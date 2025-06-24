import docx
import json

# === CONFIG ===
docx_path = "/mnt/data/crs_spfinal.docx"
output_json_path = "specification_approval_output.json"

def extract_specification_approval(file_path):
    doc = docx.Document(file_path)

    approval_data = {
        "Council/Committee": "",
        "Reference No.": "",
        "Date": ""
    }

    for para in doc.paragraphs:
        text = para.text.strip().lower()

        if "council" in text and "committee" in text:
            approval_data["Council/Committee"] = para.text.strip()
        elif "reference no" in text:
            approval_data["Reference No."] = para.text.strip()
        elif "date" in text:
            approval_data["Date"] = para.text.strip()

    return approval_data

# === RUN ===
approval_section = extract_specification_approval(docx_path)

with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(approval_section, f, ensure_ascii=False, indent=2)

print("✅ Specification Approval section extracted and saved to:", output_json_path)
