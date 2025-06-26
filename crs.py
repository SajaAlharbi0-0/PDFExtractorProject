import os
import json

# ✅ Unified extractor for Course Info + Section A
from Crs_Section_Info_A import extract_course_data
# These remain unchanged
from Crs_Section_C import extract_course_topics_from_docx
from Crs_Section_D import extract_section_d, extract_text_from_docx as d_text
from Crs_Section_E import extract_section_e_from_docx
from Crs_Section_F_G import extract_F_and_G
from Crs_Section_B import extract_clos2

def extract_course_to_json(docx_path):
    ab = extract_course_data(docx_path)
    section_a_data = {
        "Course Info": {
            "Course Title": ab.get("Course Title", ""),
            "Course Code": ab.get("Course Code", ""),
            "Program": ab.get("Program", ""),
            "Department": ab.get("Department", ""),
            "Faculty": ab.get("Faculty", ""),
            "Institution": ab.get("Institution", ""),
            "Version": ab.get("Version", ""),
            "Last Revision Date": ab.get("Last Revision Date", "")
        },
        "Sections": {
            "A": {
                "title": "General information about the course",
                "content": {
                    "1. Course Identification": {
                        "1. Credit hours": ab.get("Credit Hours", ""),
                        "2. Course type": {
                            "A.": ab.get("Course Type A", []),
                            "B.": ab.get("Course Type B", [])
                        },
                        "3. Level/year at which this course is offered": ab.get("Level/Year", "")
                    },
                    "2. Course Description": ab.get("Course Description", ""),
                    "3. Pre-requisites": ab.get("Pre-requisites", ""),
                    "4. Co-requisites": ab.get("Co-requisites", ""),
                    "5. Course Main Objectives": ab.get("Course Main Objectives", ""),
                    "6. Modes of Instruction": ab.get("Teaching Modes", []),
                    "7. Activities": ab.get("Activities", [])
                }
            }
        }
    }

    section_b = extract_clos2(docx_path)
    section_c = extract_course_topics_from_docx(docx_path)
    doc_d, text_d = d_text(docx_path)
    section_d = extract_section_d(doc_d, text_d)
    section_e = extract_section_e_from_docx(docx_path)
    section_fg = extract_F_and_G(docx_path)

    full = section_a_data
    full["Sections"]["B"] = section_b
    full["Sections"]["C"] = {"title": "Course Content (Topics)", "content": section_c}
    full["Sections"]["D"] = {"title": "Student Assessment", "content": section_d.get("Student Assessment", {})}
    full["Sections"]["E"] = {"title": "Learning Resources and Facilities", "content": section_e}
    full["Sections"]["F"] = {"title": "Assessment of Course Quality", "content": section_fg.get("Assessment of Course Quality", {})}
    full["Sections"]["G"] = {"title": "Specification Approval", "content": section_fg.get("Specification Approval", {})}

    return full