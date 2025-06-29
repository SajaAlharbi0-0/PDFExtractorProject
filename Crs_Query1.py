import re
from firebase_config import db

def get_assessment_data(department, code=None):
    department = department.strip().upper()
    code = code.strip() if code else ""

    all_labels = []
    all_values = []

    try:
        collection = db.collection("course_specification").stream()
    except Exception as e:
        return {"status": "error", "message": f"Firebase error: {e}"}

    for doc in collection:
        doc_data = doc.to_dict().get("data", {})
        course_code = doc_data.get("Course Info", {}).get("Course Code", "").replace(" ", "").upper()

        if not course_code.startswith(department):
            continue
        if code and not course_code.endswith(code):
            continue

        try:
            assessments = doc_data["Sections"]["D"]["content"]["Assessment Activities"]
        except KeyError:
            continue

        labels = []
        values = []

        for a in assessments:
            activity = a.get("Activity", "").strip()
            score_str = re.sub(r'[^0-9.]', '', a.get("Score", ""))
            if not activity or not score_str:
                continue
            try:
                values.append(float(score_str))
                labels.append(activity)
            except ValueError:
                continue

        if not labels or not values:
            continue

        # ✅ return early if one course
        if code:
            return {
                "status": "success",
                "isSingleCourse": True,
                "chartTitle": f"Assessment Distribution - {course_code}",
                "data": {
                    "labels": labels,
                    "values": values
                }
            }

        # aggregate all courses
        all_labels.extend([f"{course_code}: {label}" for label in labels])
        all_values.extend(values)

    if not all_labels:
        return {"status": "error", "message": "No valid assessment data found."}

    return {
        "status": "success",
        "isSingleCourse": False,
        "chartTitle": f"Assessment Distribution for {department}",
        "data": {
            "labels": all_labels,
            "values": all_values
        }
    }
