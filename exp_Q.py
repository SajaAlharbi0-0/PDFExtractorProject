import json
from firebase_config import db
def load_location_chart(department, subject_code):
    print(f"🔍 department = {department}, subject_code = {subject_code}")
    result_text = ""
    is_single = False

    collection = db.collection("field_experience").stream()

    for doc in collection:
        data = doc.to_dict().get("data", {})
        course_code = data.get("General Info", {}).get("Course Code", "").replace(" ", "").upper()
        print(f"➡️ Checking course_code: {course_code}")

        if not course_code.startswith(department.upper()):
            print(f"⛔ Skipping {course_code} (not matching department)")
            continue
        if subject_code and not course_code.endswith(subject_code):
            print(f"⛔ Skipping {course_code} (not matching subject_code)")
            continue

        is_single = bool(subject_code)

        try:
            locations = data["C. Field Experience Administration"]["3. Field Experience Location Requirements"]
            locations = [loc.get("Location", "").strip() for loc in locations if loc.get("Location", "").strip()]
            if locations:
                result_text += f"""
                <div style="margin-bottom: 15px;">
                    <div style="font-weight: bold; font-size: 16px; margin-bottom: 5px;">
                        📍 Training Locations for {course_code}:
                    </div>
                    <div style="font-family: monospace; line-height: 1.7;">
                        {"<br>".join(f"- {name}" for name in locations)}
                    </div>
                </div>
                """
        except Exception as e:
            print(f"⚠️ Error reading locations: {e}")
            continue

    if not result_text:
        result_text = "<p>No training locations found for the selected criteria.</p>"

    return {
        "status": "success",
        "isSingleCourse": is_single,
        "html": result_text,
        "chartTitle": "Training Locations"
    }


def load_clo_group_chart(department, subject_code):
    print(f"📊 CLO Group Chart: dept={department}, subject={subject_code}")
    
    clo_groups = [
        "1.0 Knowledge and understanding",
        "2.0 Skills",
        "3.0 Values, autonomy, and responsibility"
    ]
    group_totals = {group: 0 for group in clo_groups}
    is_single = False

    collection = db.collection("field_experience").stream()

    for doc in collection:
        data = doc.to_dict().get("data", {})
        course_code = data.get("General Info", {}).get("Course Code", "").replace(" ", "").upper()

        if not course_code.startswith(department.upper()):
            continue

        if subject_code:
            if not course_code.endswith(subject_code):
                continue
            is_single = True

        try:
            clos_section = data.get("B. CLOs", {})
            for group in clo_groups:
                group_totals[group] += len(clos_section.get(group, []))
        except Exception as e:
            print(f"⚠️ Error in CLO group extraction: {e}")
            continue

    return {
        "status": "success",
        "isSingleCourse": is_single,
        "data": {
            "labels": list(group_totals.keys()),
            "values": list(group_totals.values())
        },
        "chartTitle": "CLO Count By Group"
    }


def load_stakeholders_chart(department, subject_code):
    print(f"📊 Stakeholders Chart: dept={department}, subject={subject_code}")

    stakeholders = [
    "Department/College",
    "Field Supervisor",
    "Student",
    "Teaching Staff",
    "Training Organization"
]

    activity_set = set()
    points = []
    is_single = False

    collection = db.collection("field_experience").stream()

    for doc in collection:
        data = doc.to_dict().get("data", {})
        course_code = data.get("General Info", {}).get("Course Code", "").replace(" ", "").upper()

        if not course_code.startswith(department.upper()):
            continue

        if subject_code:
            if not course_code.endswith(subject_code):
                continue
            is_single = True

        rows = data.get("C. Field Experience Administration", {}) \
                   .get("2. Distribution of Responsibilities for Field Experience Activities", [])

        for row in rows:
            activity = row.get("Activity", "").strip()
            if not activity:
                continue

            activity_set.add(activity)
            for s in stakeholders:
                if row.get(s, "").strip() == "√":
                    points.append({ "x": s, "y": activity })

    return {
        "status": "success",
        "isSingleCourse": is_single,
        "data": {
            "labels": list(activity_set),
            "values": points
        },
        "chartTitle": f"Stakeholder Activity Map{f' - {subject_code}' if subject_code else ''}"
    }




def load_evaluation_chart(department, subject_code):
    print(f"📊 Evaluation Chart: dept={department}, subject={subject_code}")

    direct = 0
    indirect = 0
    is_single = False

    collection = db.collection("field_experience").stream()

    for doc in collection:
        data = doc.to_dict().get("data", {})
        course_code = data.get("General Info", {}).get("Course Code", "").replace(" ", "").upper()

        if not course_code.startswith(department.upper()):
            continue

        if subject_code:
            if not course_code.endswith(subject_code):
                continue
            is_single = True

        evaluations = data.get("D. Evaluation", {}) \
                          .get("Training Quality Evaluation", [])

        for item in evaluations:
            method = item.get("Evaluation Method", "").strip().lower()
            if method.startswith("direct"):
                direct += 1
            elif method.startswith("indirect"):
                indirect += 1

    # ⚠️ حالة عدم وجود أي تقييم مباشر أو غير مباشر
    if direct == 0 and indirect == 0:
        return {
            "status": "success",
            "isSingleCourse": is_single,
            "html": f"""
                <div style='padding:2rem;text-align:center'>
                  <h3 style='color:#d15600'>⚠️ Invalid Evaluation Format</h3>
                  <p>No evaluation methods found in recognizable 'Direct' or 'Indirect' format.</p>
                </div>
            """,
            "data": {
                "labels": [],
                "values": []
            },
            "chartTitle": "Evaluation Method Types"
        }

    return {
        "status": "success",
        "isSingleCourse": is_single,
        "data": {
            "labels": ["Direct", "Indirect"],
            "values": [direct, indirect]
        },
        "chartTitle": f"Evaluation Method Types{f' - {subject_code}' if subject_code else ''}"
    }
