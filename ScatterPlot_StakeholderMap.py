import json
import matplotlib.pyplot as plt

# --- ربط كل كورس بملفه ---
course_files = {
    "BIO390": "field_exp_sp(final)_extracted.json",
    "FNU484": "field_exp sp3_extracted.json"
   #"FNU473": "fnu473_extracted.json"  # أضف باقي الملفات هنا
}

# --- الجهات المعنية ---
stakeholders = ["Department/College", "Teaching Staff", "Student", "Training Organization", "Field Supervisor"]

# --- إدخال المستخدم ---
department = input("Enter Department (BIO / FNU): ").strip().upper()
code = input("Enter Course Code (390 / 484 / 473) [Optional]: ").strip()

# --- تحديد المفاتيح المستهدفة ---
if code:
    course_key = department + code
    if course_key in course_files:
        target_keys = [course_key]
    else:
        print(f"❌ No file found for {course_key}")
        exit()
else:
    # إذا لم يُدخل الكود، اختر جميع المواد التابعة للقسم
    target_keys = [k for k in course_files if k.startswith(department)]
    if not target_keys:
        print(f"❌ No courses found for department {department}")
        exit()

# --- عرض الرسومات ---
for key in target_keys:
    json_file = course_files[key]

    try:
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)

        resp = data["C.\tField Experience Administration"]["2. Distribution of Responsibilities for Field Experience Activities"]

        activities_by_stakeholder = {s: [] for s in stakeholders}
        for row in resp:
            activity = row["Activity"]
            for s in stakeholders:
                if row[s].strip() == "√":
                    activities_by_stakeholder[s].append(activity)

        all_activities = sorted(set(
            act for acts in activities_by_stakeholder.values() for act in acts
        ))

        matrix = []
        for act in all_activities:
            row = []
            for s in stakeholders:
                row.append(1 if act in activities_by_stakeholder[s] else 0)
            matrix.append(row)

        # --- رسم Scatter Plot ---
        plt.figure(figsize=(12, 6))
        for i, activity in enumerate(all_activities):
            for j, stakeholder in enumerate(stakeholders):
                if matrix[i][j] == 1:
                    plt.scatter(j, i, color='blue')

        plt.xticks(range(len(stakeholders)), stakeholders, rotation=45)
        plt.yticks(range(len(all_activities)), all_activities)
        plt.title(f"Stakeholder Activity Map - {key}")
        plt.xlabel("Stakeholders")
        plt.ylabel("Activities")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(0.5)

    except Exception as e:
        print(f"❌ Error in {json_file}: {e}")

input("↩️ Press Enter to close all charts...")
