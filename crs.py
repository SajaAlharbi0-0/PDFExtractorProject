import pdfplumber
import json
import re

# Paths
pdf_path = "C:\\Users\\mahaf\\Downloads\\crs sp1.pdf"
output_json_path = "C:\\Users\\mahaf\\Downloads\\all_courses_updated.json"

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
        "B": {
            "title": "Course Learning Outcomes (CLOs), Teaching Strategies and Assessment Methods",
            "content": {
                "1.0 Knowledge and understanding": [],
                "2.0 Skills": [],
                "3.0 Values, autonomy, and responsibility": []
            }
        }, "D": {
        "title": "Students Assessment Activities",
        "content": []
    },
    "E": {
        "title": "Learning Resources and Facilities",
        "content": {
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
    },
    "F": {
    "title": "Assessment of Course Quality",
    "content": {
        "assessment_of_course_quality": []
    }
},
"G": {
    "title": "Specification Approval",
    "content": {
        "COUNCIL /COMMITTEE": "",
        "REFERENCE NO.": "",
        "DATE": ""
    }
}



    }
}
# Extract from PDF
with pdfplumber.open(pdf_path) as pdf:
    full_text = "\n".join(page.extract_text() for page in pdf.pages)

# Extract CLOs from Section B using improved regex
clo_matches = re.findall(
    r"(?P<code>\d\.\d)\s+(?P<outcome>.+?)\s+Activities;\s*(?P<strategy>.+?)\s+(Midterms.*?|Final Exam.*?)\s*(?=\d\.\d|\Z)",
    full_text,
    re.DOTALL
)

# Debug check (optional)
print("=== Sample from text ===")
print(full_text[full_text.find("1.0 Knowledge and understanding"):][:500])  # Print preview

# Assign CLOs to their categories
for match in clo_matches:
    clo_code = match[0]
    outcome = match[1]
    strategy = match[2]
    assessment = match[3]

    group_key = {
        "1": "1.0 Knowledge and understanding",
        "2": "2.0 Skills",
        "3": "3.0 Values, autonomy, and responsibility"
    }.get(clo_code[0], None)

    if group_key:
        data_structure["Sections"]["B"]["content"][group_key].append({
            "Code": clo_code.strip(),
            "Course Learning Outcome": outcome.strip().replace("\n", " "),
            "PLO Code": "",  # Leave blank or fill later
            "Teaching Strategies": strategy.strip(),
            "Assessment Methods": assessment.strip()
        })




    




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

# Teaching mode
teaching_mode_match = re.search(r"1\s+Traditional classroom\s+(\d+)\s+(\d+%)", full_text)
if teaching_mode_match:
    hours = teaching_mode_match.group(1)
    percent = teaching_mode_match.group(2)
    data_structure["Sections"]["A"]["content"]["2. Teaching mode"]["Traditional classroom"]["Contact Hours"] = int(hours)
    data_structure["Sections"]["A"]["content"]["2. Teaching mode"]["Traditional classroom"]["Percentage"] = percent

# Contact Hours
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

# Here is the Section C code
##################################################################################################################

##################################################################################################################
# === Section D: Students Assessment Activities ===
def extract_assessment_activities(text):
    pattern = r"\d+\.\s+(.*?)\s+(TBA|\d+)\s+(\d+%)"
    matches = re.findall(pattern, text)
    activities = []
    for activity, week, percent in matches:
        activities.append({
            "activity": activity.strip(),
            "week": week.strip(),
            "percentage": percent.strip()
        })
    return activities

data_structure["Sections"]["D"]["content"] = extract_assessment_activities(full_text)




# === Section E: Learning Resources and Facilities ===
def clean_reference_block(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return [" ".join(lines)] if lines else []

essential_match = re.search(r"Essential References\s*(.+?)\s*(Supportive References|Electronic Materials)", full_text, re.DOTALL)
if essential_match:
    data_structure["Sections"]["E"]["content"]["References and Learning Resources"]["Essential References"] = clean_reference_block(essential_match.group(1))

supportive_match = re.search(r"Supportive References\s*(.+?)\s*(Electronic Materials|Other Learning Materials)", full_text, re.DOTALL)
if supportive_match:
    data_structure["Sections"]["E"]["content"]["References and Learning Resources"]["Supportive References"] = clean_reference_block(supportive_match.group(1))

electronic_match = re.search(r"Electronic Materials\s*(.+?)\s*(Other Learning Materials|Required Facilities and Equipment)", full_text, re.DOTALL)
if electronic_match:
    data_structure["Sections"]["E"]["content"]["References and Learning Resources"]["Electronic Materials"] = clean_reference_block(electronic_match.group(1))

other_match = re.search(r"Other Learning Materials\s*(.+?)\s*(Required Facilities and Equipment|6\. Required Facilities and Equipment)", full_text, re.DOTALL)
if other_match:
    data_structure["Sections"]["E"]["content"]["References and Learning Resources"]["Other Learning Materials"] = clean_reference_block(other_match.group(1))

facilities_match = re.search(r"Facilities\s*:\s*(.+?)\s*Technology equipment", full_text, re.DOTALL)
if facilities_match:
    data_structure["Sections"]["E"]["content"]["Required Facilities and Equipment"]["Facilities"] = facilities_match.group(1).strip().replace("\n", " ")

tech_match = re.search(r"Technology equipment\s*:\s*(.+?)\s*Other equipment", full_text, re.DOTALL)
if tech_match:
    data_structure["Sections"]["E"]["content"]["Required Facilities and Equipment"]["Technology equipment"] = tech_match.group(1).strip().replace("\n", " ")

other_eq_match = re.search(r"Other equipment\s*:\s*(.+?)\s*(\n|$)", full_text, re.DOTALL)
if other_eq_match:
    data_structure["Sections"]["E"]["content"]["Required Facilities and Equipment"]["Other equipment"] = other_eq_match.group(1).strip().replace("\n", " ")


####################################################################################################################################
# === Section F: Assessment of Course Quality ===
# === Section F using fresh read with PyMuPDF ===
#############################################################
# === Section F: Parser that merges broken area names ===

def parse_section_f_from_file(pdf_path):
    import fitz, re

    print("\n🔍 [DEBUG] Entering parse_section_f_from_file()")

    # 1) Open PDF and locate real table
    doc = fitz.open(pdf_path)
    section_text = ""
    for pno, page in enumerate(doc, start=1):
        txt = page.get_text()
        if "Assessment Areas/Issues" in txt:
            section_text = txt
            print(f" [DEBUG] Found table on page {pno}")
            break
    if not section_text:
        print(" [DEBUG] Table header not located")
        return {"assessment_of_course_quality": []}

    # 2) Normalize lines
    lines = [ln.strip() for ln in section_text.splitlines() if ln.strip()]
    # 3) Find header index
    header_idx = next((i for i, ln in enumerate(lines)
                       if "Assessment Areas/Issues" in ln), None)
    if header_idx is None:
        print(" [DEBUG] Header index missing")
        return {"assessment_of_course_quality": []}
    table_lines = lines[header_idx+1:]
    print("[DEBUG] Raw table lines:")
    for idx, ln in enumerate(table_lines):
        print(f"  {idx:02d}: {repr(ln)}")

    # 4) Merge split area names
    fixed_areas = [
        "Effectiveness of teaching",
        "Effectiveness of Students assessment",
        "Quality of learning resources",
        "The extent to which CLOs have been achieved"
    ]

    merged = []
    i = 0
    while i < len(table_lines):
        curr = table_lines[i]
        merged_flag = False
        # try to merge with next if combined equals any fixed_area
        if i + 1 < len(table_lines):
            combo = (curr + " " + table_lines[i+1]).strip()
            for area in fixed_areas:
                if combo.lower() == area.lower():
                    merged.append(area)
                    merged_flag = True
                    i += 2
                    break
        if merged_flag:
            continue
        merged.append(curr)
        i += 1

    print("\n[DEBUG] Merged table lines:")
    for idx, ln in enumerate(merged):
        print(f"  {idx:02d}: {repr(ln)}")

    # 5) Parse each fixed area
    result = []
    for area in fixed_areas:
        print(f"\n[DEBUG] Parsing area: {area!r}")
        # find index in merged
        start_idx = next((i for i, ln in enumerate(merged)
                          if ln.lower().startswith(area.lower())), None)
        if start_idx is None:
            print(f"   [DEBUG] Area {area!r} not found")
            result.append({
                "assessment_areas_issues": area,
                "assessor": "",
                "assessment_methods": ""
            })
            continue

        # collect assessor lines
        assessor_parts = []
        j = start_idx + 1
        while j < len(merged):
            ln = merged[j]
            if any(ln.lower().startswith(a.lower()) for a in fixed_areas + ["other"]) \
               or ln.startswith("Direct:") or ln.startswith("Indirect:"):
                break
            assessor_parts.append(ln)
            j += 1
        assessor = " ".join(assessor_parts).strip()
        print(f"  [DEBUG] assessor_parts={assessor_parts!r} => {assessor!r}")

        # collect methods
        direct = ""
        indirect = ""
        if j < len(merged) and merged[j].startswith("Direct:"):
            direct = merged[j]; j += 1
        if j < len(merged) and merged[j].startswith("Indirect:"):
            indirect = merged[j]; j += 1
        methods = " ".join([direct, indirect]).strip()
        print(f"  [DEBUG] methods_direct={direct!r}, indirect={indirect!r} => {methods!r}")

        result.append({
            "assessment_areas_issues": area,
            "assessor": assessor,
            "assessment_methods": methods
        })

    # 6) Append Other
    result.append({
        "assessment_areas_issues": "Other",
        "assessor": "None",
        "assessment_methods": "None"
    })

    print("\n🔍 [DEBUG] Finished parsing Section F\n")
    return {"assessment_of_course_quality": result}

# — Plug it in:
data_structure["Sections"]["F"]["content"] = parse_section_f_from_file(pdf_path)
#############################################################





####################################################################################################################################
# === Section G: Specification Approval ===
section_g_match = re.search(r"G\. Specification Approval.*?(COUNCIL.*?)(REFERENCE NO\..*?)(DATE.+)", full_text, re.DOTALL)
if section_g_match:
    council = section_g_match.group(1).replace("COUNCIL /COMMITTEE", "").strip()
    reference = section_g_match.group(2).replace("REFERENCE NO.", "").strip()
    date = section_g_match.group(3).replace("DATE", "").strip()

    data_structure["Sections"]["G"]["content"] = {
        "COUNCIL /COMMITTEE": council,
        "REFERENCE NO.": reference,
        "DATE": date
    }
####################################################################################################################################




# === Save JSON ===
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(data_structure, f, ensure_ascii=False, indent=2)

print("Saved to:", output_json_path)
