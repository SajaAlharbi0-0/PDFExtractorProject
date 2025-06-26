import json
import matplotlib.pyplot as plt
from collections import defaultdict

# --- ملفات الكورسات ---
course_files = {
    "STAT110": "crs sp1 (1).json",
    "PHYS110": "crs_sp2 (1).json",
    "BIO241": "crs_sp3.json",
    "BIO491": "crs sp4.json"
}

# --- إدخال المستخدم: القسم فقط ---
user_dept = input("Enter Department (STATISTICS / PHYSICS / DEPARTMENT OF BIOLOGICAL SCIENCES): ").strip().lower()

# --- تجميع البيانات للقسم المحدد ---
required = 0
elective = 0
matched_dept_name = ""

for key, filename in course_files.items():
    try:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)

        dept_name = data["Course Info"]["Department"].strip().lower()
        course_type = data["Sections"]["A"]["content"]["1. Course Identification"]["2. Course type"].get("B.", "").strip()

        if user_dept in dept_name:
            matched_dept_name = data["Course Info"]["Department"]
            if course_type == "Required":
                required += 1
            elif course_type == "Elective":
                elective += 1

    except Exception as e:
        print(f"⚠️ Error in {filename}: {e}")

# --- التحقق من النتائج ---
if required == 0 and elective == 0:
    print("❌ No matching courses found for that department.")
    exit()

# --- رسم الرسم البياني ---
plt.figure(figsize=(6, 5))
plt.bar(["Required", "Elective"], [required, elective], color=["steelblue", "darkorange"])
plt.title(f"Required vs Elective Courses in {matched_dept_name}")
plt.ylabel("Number of Courses")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
