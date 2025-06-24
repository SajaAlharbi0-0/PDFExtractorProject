import json
import re
from docx import Document

# ==== CONFIG ====
docx_path = r"C:\Users\mahaf\Downloads\crs sp2.w.docx"
output_json_path = r"C:\Users\mahaf\Downloads\section_d_only.json"

# ==== UTILITY FUNCTIONS ====
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
    return doc, full_text

# ==== SECTION D EXTRACTION ONLY ====
def extract_section_d(doc, text):
    data = {
        "Student Assessment": {
            "Assessment Activities": [],
            "Assessment Methods": [],
            "Grading Distribution": "",
            "Final Exam Description": ""
        }
    }

    # ========== Assessment Activities Table ==========
    for table in doc.tables:
        if table.rows and len(table.rows) > 1:
            headers = [cell.text.strip().lower() for cell in table.rows[0].cells]
            if len(headers) > 1 and "assessment activities" in headers[1]:
                for row in table.rows[1:]:
                    cells = row.cells
                    if len(cells) >= 3:
                        activity = cells[1].text.strip()
                        timing = cells[2].text.strip()
                        score = cells[3].text.strip() if len(cells) > 3 else ""
                        data["Student Assessment"]["Assessment Activities"].append({
                            "Activity": activity,
                            "Timing": timing,
                            "Score": score
                        })
                break  # Only the first matching table is needed

    # ========== Text-Based Extraction ==========
    assessment_pattern = r"4[\.\s]*Student Assessment(.+?)5[\.\s]*Learning Resources and Facilities"
    assess_match = re.search(assessment_pattern, text, re.DOTALL | re.IGNORECASE)
    if assess_match:
        assess_text = assess_match.group(1)

        method_match = re.findall(r"(Quiz|Assignment|Midterm|Final)", assess_text, re.IGNORECASE)
        data["Student Assessment"]["Assessment Methods"] = list(set(method_match))

        grading_match = re.search(r"Grading.*?(\d{1,3}%?.+?)\n", assess_text)
        if grading_match:
            data["Student Assessment"]["Grading Distribution"] = grading_match.group(1).strip()

        final_match = re.search(r"Final Exam.*?:\s*(.+)", assess_text)
        if final_match:
            data["Student Assessment"]["Final Exam Description"] = final_match.group(1).strip()

    return data

# ==== EXECUTION ====
doc, text = extract_text_from_docx(docx_path)
section_d_data = extract_section_d(doc, text)

with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(section_d_data, f, ensure_ascii=False, indent=2)

print("✅ Extracted Section D saved to:", output_json_path)
