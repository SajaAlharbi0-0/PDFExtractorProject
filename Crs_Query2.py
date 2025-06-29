import json

# --- ملفات الكورسات ---
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

def get_learning_outcomes(department, code=None):
    department = department.strip().upper()
    code = code.strip() if code else ""

    if code:
        course_key = department + code
        if course_key not in course_files:
            return {"status": "error", "message": f"No file found for {course_key}"}
        target_keys = [course_key]
    else:
        target_keys = [k for k in course_files if k.startswith(department)]
        if not target_keys:
            return {"status": "error", "message": f"No courses found for department {department}"}

    results = []

    for key in target_keys:
        json_file = course_files[key]

        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)

            sections_b = data["Sections"]["B"]

            course_results = []

            for outcomes_list in sections_b.values():
                if not outcomes_list:
                    continue
                for outcome in outcomes_list:
                    clo = outcome.get("Course Learning Outcome", "").strip()
                    assessment = outcome.get("Assessment Methods", "").strip()
                    if clo:
                        course_results.append({
                            "outcome": clo,
                            "assessment": assessment
                        })

            results.append({
                "course": key,
                "data": course_results
            })

        except Exception as e:
            return {"status": "error", "message": f"Error in {json_file}: {e}"}

    return {"status": "success", "data": results}
