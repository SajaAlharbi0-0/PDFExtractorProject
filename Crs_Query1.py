import json

# ربط كل كورس بملفه
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
    "BIO444": "crs sp8.json"
}


def get_assessment_data(department, code=None):
    department = department.upper()
    target_keys = []

    if code:
        course_key = department + code
        if course_key in course_files:
            target_keys = [course_key]
        else:
            return {"status": "error", "message": f"No file found for {course_key}"}
    else:
        target_keys = [k for k in course_files if k.startswith(department)]
        if not target_keys:
            return {"status": "error", "message": f"No courses found for department {department}"}

    all_data = []
    for key in target_keys:
        json_file = course_files[key]

        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)

            assessments = data["Sections"]["D"]["content"]["Assessment Activities"]
            names = [a["Activity"] for a in assessments]
            scores = []

            for a in assessments:
                score_str = a["Score"].replace('%', '').strip()
                try:
                    scores.append(float(score_str))
                except ValueError:
                    continue

            if not scores:
                continue

            all_data.append({
                "course": key,
                "labels": names,
                "values": scores
            })

        except Exception as e:
            return {"status": "error", "message": f"Error in {json_file}: {e}"}

    if not all_data:
        return {"status": "error", "message": "No valid score data found."}

    return {
        "status": "success",
        "isSingleCourse": len(all_data) == 1,
        "data": all_data
    }
