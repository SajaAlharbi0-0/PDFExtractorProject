
import pdfplumber
import json
import re

# Paths
pdf_path = "C:\\Users\\sajaa\\Downloads\\crs sp1.pdf"
output_json_path = "C:\\Users\\sajaa\\Downloads\\all_courses_updated.json"

# Updated data structure
data_structure = {
    "Course Info": {
        "Course Title": "",
        "Course Code": "",
        "Program": "",
        "Department": "",
        "Faculty": "",
        "University": "",
        "Version": "",
        "Last Revision Date": ""
    },
    "Sections": {
        "A": {
            "title": "General information about the course",
            "content": {
                "1. Course Identification": {
                    "1. Credit hours": "",
                    "2. Course type": {
                        "A.": [],
                        "B.": []
                    },
                    "3. Level/year": "",
                    "4. Course general Description": "",
                    "5. Pre-requirements": "",
                    "6. Co-requirements": "",
                    "7. Course Main Objective(s)": ""
                },
                "2. Teaching mode": {
                    "Traditional classroom": {
                        "Contact Hours": None,
                        "Percentage": None
                    },
                    "E-learning": {
                        "Contact Hours": None,
                        "Percentage": None
                    },
                    "Hybrid • Traditional classroom • E-learning": {
                        "Contact Hours": None,
                        "Percentage": None
                    },
                    "Distance learning": {
                        "Contact Hours": None,
                        "Percentage": None
                    }
                },
                "3. Contact Hours": {
                    "Lectures": None,
                    "Laboratory/Studio": None,
                    "Field": None,
                    "Tutorial": None,
                    "Others (…)": None,
                    "Total": None
                }

            }
        },
        "B": {"title": "Course Learning Outcomes (CLOs), Teaching Strategies and Assessment", "content": None},
        "C": {"title": "Course Content", "content": None},
        "D": {"title": "Students Assessment Activities", "content": None},
        "E": {"title": "Learning Resources and Facilities", "content": None},
        "F": {"title": "Assessment of Course Quality", "content": None},
        "G": {"title": "Specification Approval", "content": None}
    }
}

# Extract from PDF
with pdfplumber.open(pdf_path) as pdf:
    full_text = "\n".join(page.extract_text() for page in pdf.pages)

# Fill Course Info
patterns = {
    "Course Title": r"Course Title:\s*(.+)",
    "Course Code": r"Course Code:\s*(.+)",
    "Program": r"Program:\s*(.+)",
    "Department": r"Department:\s*(.+)",
    "Faculty": r"Faculty:\s*(.+)",
    "University": r"University:\s*(.+)",
    "Version": r"Version:\s*(.+)",
    "Last Revision Date": r"Last Revision Date:\s*(.+)"
}
for key, pattern in patterns.items():
    match = re.search(pattern, full_text)
    if match:
        data_structure["Course Info"][key] = match.group(1).strip()

# Section A.1
credit = re.search(r"1\. Credit hours:\s*\((.*?)\)", full_text)
if credit:
    data_structure["Sections"]["A"]["content"]["1. Course Identification"]["1. Credit hours"] = credit.group(1).strip()

if "☒ Required" in full_text:
    data_structure["Sections"]["A"]["content"]["1. Course Identification"]["2. Course type"]["B."].append("Required")
if "☐ Elective" in full_text:
    data_structure["Sections"]["A"]["content"]["1. Course Identification"]["2. Course type"]["B."].append("Elective")
if "☒ Faculty" in full_text:
    data_structure["Sections"]["A"]["content"]["1. Course Identification"]["2. Course type"]["A."].append("Faculty")

level = re.search(r"3\. Level/year.*?:\s*(.+)", full_text)
if level:
    data_structure["Sections"]["A"]["content"]["1. Course Identification"]["3. Level/year"] = level.group(1).strip()

desc = re.search(r"4\. Course general Description:\s*(.+?)\s*5\.", full_text, re.DOTALL)
if desc:
    data_structure["Sections"]["A"]["content"]["1. Course Identification"]["4. Course general Description"] = desc.group(1).strip()

pre = re.search(r"5\. Pre-requirements.*?:\s*(.+?)\s*6\.", full_text, re.DOTALL)
if pre:
    data_structure["Sections"]["A"]["content"]["1. Course Identification"]["5. Pre-requirements"] = pre.group(1).strip()

co = re.search(r"6\. Co-requirements.*?:\s*(.+?)\s*7\.", full_text, re.DOTALL)
if co:
    data_structure["Sections"]["A"]["content"]["1. Course Identification"]["6. Co-requirements"] = co.group(1).strip()

obj = re.search(r"7\. Course Main Objective\(s\):\s*(.+?)\s*2\.", full_text, re.DOTALL)
if obj:
    data_structure["Sections"]["A"]["content"]["1. Course Identification"]["7. Course Main Objective(s)"] = obj.group(1).strip()

# Teaching mode (read only Traditional classroom hours and percentage from table)
teaching_mode_match = re.search(r"1\s+Traditional classroom\s+(\d+)\s+(\d+%)", full_text)
if teaching_mode_match:
    hours = teaching_mode_match.group(1)
    percent = teaching_mode_match.group(2)
    data_structure["Sections"]["A"]["content"]["2. Teaching mode"]["Traditional classroom"]["Contact Hours"] = int(hours)
    data_structure["Sections"]["A"]["content"]["2. Teaching mode"]["Traditional classroom"]["Percentage"] = percent
# Contact Hours (based on academic semester) – Read values from table
contact_hour_match = re.search(
    r"1\.\s*Lectures\s+(\d+)\s*2\.\s*Laboratory/Studio\s+(\d+)?\s*3\.\s*Field\s+(\d+)?\s*4\.\s*Tutorial\s+(\d+)?\s*5\.\s*Others.*?\s*(\d+)?\s*Total\s+(\d+)",
    full_text
)

if contact_hour_match:
    data_structure["Sections"]["A"]["content"]["3. Contact Hours"]["Lectures"] = int(contact_hour_match.group(1))
    data_structure["Sections"]["A"]["content"]["3. Contact Hours"]["Laboratory/Studio"] = int(contact_hour_match.group(2)) if contact_hour_match.group(2) else None
    data_structure["Sections"]["A"]["content"]["3. Contact Hours"]["Field"] = int(contact_hour_match.group(3)) if contact_hour_match.group(3) else None
    data_structure["Sections"]["A"]["content"]["3. Contact Hours"]["Tutorial"] = int(contact_hour_match.group(4)) if contact_hour_match.group(4) else None
    data_structure["Sections"]["A"]["content"]["3. Contact Hours"]["Others (…)"] = int(contact_hour_match.group(5)) if contact_hour_match.group(5) else None
    data_structure["Sections"]["A"]["content"]["3. Contact Hours"]["Total"] = int(contact_hour_match.group(6))

# Save
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(data_structure, f, ensure_ascii=False, indent=2)

output_json_path
