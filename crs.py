import fitz  # PyMuPDF
import json
import re

pdf_path = "C:/Users/mahaf/Downloads/crs sp2.pdf"
excel_output = "C:/Users/mahaf/Downloads/cleaned_output.xlsx"

def extract_data_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = "\n".join(page.get_text() for page in doc)

    def extract_with_regex(pattern, default=None):
        match = re.search(pattern, full_text, re.IGNORECASE)
        return match.group(1).strip() if match else default

    data = {
        "Course Title": extract_with_regex(r"Course Title:\s+(.*?)\n"),
        "Course Code": extract_with_regex(r"Course Code:\s+(.*?)\n"),
        "Program": extract_with_regex(r"Program:\s+(.*?)\n"),
        "Department": extract_with_regex(r"Department:\s+(.*?)\n"),
        "Faculty": extract_with_regex(r"Faculty:\s+(.*?)\n"),
        "University": extract_with_regex(r"University:\s+(.*?)\n"),
        "Version": extract_with_regex(r"Version:\s+(.*?)\n"),
        "Last Revision Date": extract_with_regex(r"Last Revision Date:\s+(.*?)\n"),
        "Credit Hours": extract_with_regex(r"Credit hours:\s*\(\s*(\d+)\s*\)"),
        "Required": bool(re.search(r"B\.\s*☒\s*Required", full_text)),
        "Pre-requirements": extract_with_regex(r"Pre-requirements for this course \(if any\):\s+(.*?)\n"),
        "Co-requirements": extract_with_regex(r"Co-requirements for this course \(if any\):\s+(.*?)\n"),
        "Main Objective": extract_with_regex(r"Course Main Objective\(s\):\s+(.*?)\n\n", default="").replace("\n", " ").strip(),
        "Teaching Modes": [],
        "Assessment": [],
        "Essential Reference": extract_with_regex(r"Essential References\s+(.*?)\n", default=""),
        "Electronic Material": extract_with_regex(r"Electronic Materials\s+(.*?)\n", default=""),
        "Facilities": {
            "Classroom": extract_with_regex(r"Facilities\s+\(Classrooms.*?\)\s+(.*?)\n", default=""),
            "Equipment": extract_with_regex(r"Technology equipment\s+\(projector.*?\)\s+(.*?)\n", default="").split(", "),
        },
        "Approval": {
            "Council": extract_with_regex(r"COUNCIL /COMMITTEE\s+(.*?)\n", default=""),
            "Reference": extract_with_regex(r"REFERENCE NO.\s+(.*?)\n", default=""),
            "Date": extract_with_regex(r"DATE\s+(.*?)\n", default=""),
        }
    }

    # Teaching Modes Table
    teaching_modes = re.findall(r"1\s+Traditional classroom\s+(\d+)\s+(\d+%)", full_text)
    if teaching_modes:
        data["Teaching Modes"].append({
            "Mode": "Traditional classroom",
            "Hours": int(teaching_modes[0][0]),
            "Percentage": teaching_modes[0][1]
        })

    # Assessment Section
    assessments = re.findall(r"\d+\.\s+([^\n]+)\s+(\d+|TBA)\s+(\d+%)", full_text)
    for a in assessments:
        data["Assessment"].append({
            "Activity": a[0].strip(),
            "Week": a[1],
            "Weight": a[2]
        })

    return data

# Usage
pdf_file ="C:/Users/mahaf/Downloads/crs sp2.pdf"

output_file = "output_course_data.json"

course_data = extract_data_from_pdf(pdf_file)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(course_data, f, indent=4, ensure_ascii=False)

print(f"✅ Data extracted and saved to {output_file}")
