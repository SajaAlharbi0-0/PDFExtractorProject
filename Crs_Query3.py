import json
from collections import defaultdict

# ملفات الكورسات (تأكد المسارات صحيحة حسب مكان تخزينها)
course_files = {
    "STAT110": "crs sp1 (1).json",
    "PHYS110": "crs_sp2 (1).json",
    "BIO241": "crs_sp3.json",
    "BIO491": "crs sp4.json",
    "FNU121": "crs sp6.json",
    "FNU471": "crs sp5.json",
    "MET450": "crs sp-elec.json",
    "MET491": "crs sp11.json",
    "FNU451": "crs sp7.json",
    "BIO444": "crs sp8.json",
}


def get_required_vs_elective(department):
    """
    department: اسم القسم (string)، مثال: BIOLOGICAL SCIENCES أو FOOD AND Nutrition
    """
    required = 0
    elective = 0
    matched_dept_name = ""

    department = department.strip().lower()

    for key, filename in course_files.items():
        try:
            with open(filename, encoding="utf-8") as f:
                data = json.load(f)

            dept_name = data["Course Info"]["Department"].strip().lower()
            course_type = data["Sections"]["A"]["content"]["1. Course Identification"]["2. Course type"].get("B.", "").strip()

            if department in dept_name:
                matched_dept_name = data["Course Info"]["Department"]
                if course_type == "Required":
                    required += 1
                elif course_type == "Elective":
                    elective += 1

        except Exception as e:
            print(f"⚠️ Error in {filename}: {e}")

    if required == 0 and elective == 0:
        return {"status": "error", "message": "No matching courses found for that department."}

    return {
        "status": "success",
        "data": {
            "required": required,
            "elective": elective,
            "department": matched_dept_name
        }
    }
