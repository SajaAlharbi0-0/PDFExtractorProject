import json
import matplotlib.pyplot as plt

# --- قائمة ملفات JSON ---
json_files = [
    "field_exp_sp(final)_extracted.json",
    "field_exp sp3_extracted.json"
]

# --- الجهات المعنية ---
stakeholders = ["Department/College", "Teaching Staff", "Student", "Training Organization", "Field Supervisor"]

# --- معالجة كل ملف ---
for json_file in json_files:
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
        plt.title(f"نقاط التوزيع - {json_file}")
        plt.xlabel("Stakeholders")
        plt.ylabel("Activities")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()

        # 👇 عرض بدون إيقاف البرنامج
        plt.show(block=False)
        plt.pause(0.5)  # تسمح له بالرسم قبل عرض التالي

    except Exception as e:
        print(f"❌ خطأ في الملف {json_file}: {e}")

# إبقاء الرسومات مفتوحة حتى المستخدم يقفلها يدويًا
input("↩️ اضغط Enter بعد الانتهاء لإغلاق جميع الرسومات...")
