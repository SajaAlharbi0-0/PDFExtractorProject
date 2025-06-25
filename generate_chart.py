import json
import matplotlib.pyplot as plt

# --- تحميل البيانات من ملف JSON ---
with open("field_exp_sp(final)_extracted.json", encoding="utf-8") as f:
    data = json.load(f)

# --- تحديد البيانات الخاصة بالأنشطة والجهات ---
resp = data["C.\tField Experience Administration"]["2. Distribution of Responsibilities for Field Experience Activities"]
stakeholders = ["Department/College", "Teaching Staff", "Student", "Training Organization", "Field Supervisor"]

# تجميع الأنشطة التي يشارك فيها كل Stakeholder
activities_by_stakeholder = {s: [] for s in stakeholders}
for row in resp:
    activity = row["Activity"]
    for s in stakeholders:
        if row[s].strip() == "√":
            activities_by_stakeholder[s].append(activity)

# --- تحضير بيانات الرسم ---
all_activities = sorted(set(
    act for acts in activities_by_stakeholder.values() for act in acts
))

# إنشاء مصفوفة علاقات (1 إذا كان مسؤول، 0 إذا لا)
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
plt.title("نقاط التوزيع بين الأنشطة والجهات المسؤولة (Stakeholders)")
plt.xlabel("Stakeholders")
plt.ylabel("Activities")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()