import json
import matplotlib.pyplot as plt

# --- ربط كل كورس بملفه ---
course_files = {
    "STAT110": "crs sp1 (1).json",
    "PHYS110": "crs_sp2.json",
    "BIO241": "crs_sp3.json",
    "BIO491": "crs sp4.json"
}

# --- إدخال المستخدم ---
department = input("Enter Department (STAT / PHYS / BIO): ").strip().upper()
code = input("Enter Course Code (110 / 241 / 491) [Optional]: ").strip()

# --- تحديد المفاتيح المستهدفة ---
if code:
    course_key = department + code
    if course_key in course_files:
        target_keys = [course_key]
    else:
        print(f"❌ No file found for {course_key}")
        exit()
else:
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

        # استخراج بيانات التقييمات من القسم D
        assessments = data["Sections"]["D"]["content"]["Assessment Activities"]
        names = [a["Activity"] for a in assessments]
        scores = []

        for a in assessments:
            score_str = a["Score"].replace('%', '').strip()
            try:
                scores.append(float(score_str))
            except ValueError:
                print(f"⚠️ Skipping invalid score '{a['Score']}' in {key}")

        if not scores:
            print(f"⚠️ No valid score data for {key}")
            continue

        # --- رسم الشارت الدائري ---
        plt.figure(figsize=(7, 7))
        plt.pie(scores, labels=names, autopct='%1.1f%%', startangle=140)
        plt.title(f"Assessment Distribution - {key}")
        plt.axis('equal')  # Make the pie chart circular
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(0.5)

    except Exception as e:
        print(f"❌ Error in {json_file}: {e}")

input("↩️ Press Enter to close all charts...")
