import docx
import json
import os



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




