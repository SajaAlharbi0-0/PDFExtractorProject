import json
import matplotlib.pyplot as plt
from pathlib import Path

# البحث عن جميع ملفات *_extracted.json
json_files = list(Path().glob("*_extracted.json"))
if not json_files:
    print("❌ لا يوجد ملفات JSON في المجلد.")
    exit()

for json_path in json_files:
    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            evaluations = data["D. Training Quality Evaluation"]["Training Quality Evaluation"]
        except Exception as e:
            print(f"❌ خطأ في قراءة الملف {json_path.name}: {e}")
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

        # ⚠ صيغة غير واضحة
        if unknown_format or (direct_count == 0 and indirect_count == 0):
            fig, ax = plt.subplots()
            msg = f"⚠ {json_path.name}\nطريقة التقييم غير مكتوبة بصيغة 'Direct' أو 'Indirect'"
            ax.text(0.5, 0.5, msg, fontsize=12, ha='center', va='center', wrap=True)
            ax.axis('off')
            plt.title("تحذير في تنسيق التقييم")
            plt.show()
        else:
            # ✅ عرض شارت
            labels = ["Direct", "Indirect"]
            sizes = [direct_count, indirect_count]

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            plt.title(f"{json_path.name} - Evaluation Method Types")
            plt.show()