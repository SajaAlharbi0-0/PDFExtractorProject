import json
import matplotlib.pyplot as plt

# --- ربط كل كورس بملفه ---
course_files = {
    "BIO390": "field_exp_sp(final)_extracted.json",
    "FNU484": "field_exp sp3_extracted.json"
    # "FNU473": "fnu473_extracted.json"  # أضف أي ملفات أخرى هنا
}

# --- أسماء مجموعات CLO ---
clo_groups = [
    "1.0 Knowledge and understanding",
    "2.0 Skills",
    "3.0 Values, autonomy, and responsibility"
]

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

        # استخراج CLOs
        clos = data["B.\tField Experience Course Learning Outcomes (CLOs), Training Activities and Assessment Methods"]

        # حساب عدد CLOs في كل مجموعة
        clo_counts = {group: len(clos.get(group, [])) for group in clo_groups}

        # --- رسم Bar Chart ---
        plt.figure(figsize=(8, 5))
        plt.bar(clo_counts.keys(), clo_counts.values(), color='skyblue')
        plt.title(f"CLO Count by Group - {key}")
        plt.xlabel("CLO Group")
        plt.ylabel("Number of CLOs")
        plt.xticks(rotation=15)
        plt.tight_layout()

        # 👇 عرض بدون إيقاف البرنامج
        plt.show(block=False)
        plt.pause(0.5)

    except Exception as e:
        print(f"❌ Error in {json_file}: {e}")

# إبقاء الرسومات مفتوحة حتى المستخدم يقفلها يدويًا
input("↩️ Press Enter to close all charts...")
