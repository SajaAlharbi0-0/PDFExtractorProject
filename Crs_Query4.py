import json
import os

# --- ربط كل كورس بملفه ---
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

# --- دالة قابلة للاستدعاء من Flask ---
def get_learning_resources(department, code=None):
    department = department.strip().upper()
    target_keys = []

    if code:
        course_key = department + code.strip()
        if course_key in course_files:
            target_keys = [course_key]
        else:
            return {"status": "error", "message": f"No file found for {course_key}"}
    else:
        target_keys = [k for k in course_files if k.startswith(department)]
        if not target_keys:
            return {"status": "error", "message": f"No courses found for department {department}"}

    results = []
    for key in target_keys:
        json_file = course_files[key]

        if not os.path.exists(json_file):
            continue

        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)

            resources = data["Sections"]["E"]["content"]["References and Learning Resources"]

            formatted_resources = {}
            for category, items in resources.items():
                formatted_resources[category] = items if items and items != ["None"] else []

            results.append({
                "course": key,
                "resources": formatted_resources
            })

        except Exception as e:
            return {"status": "error", "message": f"Error reading {json_file}: {e}"}

    return {"status": "success", "data": results}
