import json
import matplotlib.pyplot as plt
from pathlib import Path

# --- ربط كل كورس بملفه ---
course_files = {
    "BIO390": "field_exp_sp(final)_extracted.json",
    "FNU484": "field_exp sp3_extracted.json",
    "FNU473": "field_exp sp2_extracted.json"  # أضف حسب الحاجة
}

# --- إدخال المستخدم ---
department = input("Enter Department (BIO / FNU): ").strip().upper()
code = input("Enter Course Code (390 / 484 / 473) [Optional]: ").strip()

# --- تحديد الملفات المستهدفة ---
if code:
    course_key = department + code
    if course_key in course_files:
        target_files = [Path(course_files[course_key])]
    else:
        print(f"❌ No file found for {course_key}")
        exit()
else:
    target_files = [Path(course_files[k]) for k in course_files if k.startswith(department)]
    if not target_files:
        print(f"❌ No courses found for department {department}")
        exit()

# --- معالجة كل ملف ---
for json_path in target_files:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            evaluations = data["D. Training Quality Evaluation"]["Training Quality Evaluation"]
    except Exception as e:
        print(f"❌ Error reading file {json_path.name}: {e}")
        continue

    # عداد التقييمات
    direct_count = 0
    indirect_count = 0
    unknown_format = False

    for item in evaluations:
        method = item.get("Evaluation Method", "").strip().lower()
        if method.startswith("direct"):
            direct_count += 1
        elif method.startswith("indirect"):
            indirect_count += 1
        else:
            unknown_format = True
            break

    # ⚠️ إذا التنسيق غير معروف
    if unknown_format or (direct_count == 0 and indirect_count == 0):
        fig, ax = plt.subplots()
        msg = f"⚠ {json_path.name}\nThe evaluation method is not written in a recognizable 'Direct' or 'Indirect' format."
        ax.text(0.5, 0.5, msg, fontsize=12, ha='center', va='center', wrap=True)
        ax.axis('off')
        plt.title("Warning: Invalid Evaluation Format")
        plt.show()
    else:
        # ✅ رسم الرسم البياني
        labels = ["Direct", "Indirect"]
        sizes = [direct_count, indirect_count]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.title(f"{json_path.name} - Evaluation Method Types")
        plt.show()


