import json
import matplotlib.pyplot as plt

# --- قائمة ملفات JSON ---
json_files = [
    "field_exp_sp(final)_extracted.json",
    "field_exp sp3_extracted.json"
]

# --- أسماء مجموعات CLO ---
clo_groups = [
    "1.0 Knowledge and understanding",
    "2.0 Skills",
    "3.0 Values, autonomy, and responsibility"
]

# --- معالجة كل ملف ---
for json_file in json_files:
    try:
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)

        clos = data["B.\tField Experience Course Learning Outcomes (CLOs), Training Activities and Assessment Methods"]

        # نحسب عدد CLOs في كل مجموعة
        clo_counts = {group: len(clos.get(group, [])) for group in clo_groups}

        # --- رسم Bar Chart ---
        plt.figure(figsize=(8, 5))
        plt.bar(clo_counts.keys(), clo_counts.values(), color='skyblue')
        plt.title(f"عدد مخرجات التعلم (CLOs) في كل مجموعة - {json_file}")
        plt.xlabel("CLO Group")
        plt.ylabel("عدد المخرجات")
        plt.xticks(rotation=15)
        plt.tight_layout()

        # 👇 عرض بدون إيقاف البرنامج
        plt.show(block=False)
        plt.pause(0.5)

    except Exception as e:
        print(f"❌ خطأ في الملف {json_file}: {e}")

# إبقاء الرسومات مفتوحة حتى المستخدم يقفلها يدويًا
input("↩️ اضغط Enter بعد الانتهاء لإغلاق جميع الرسومات...")
