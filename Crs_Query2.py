import json

# --- ملفات الكورسات ---
course_files = {
    "STAT110": "crs sp1 (1).json",
    "PHYS110": "crs_sp2 (1).json",
    "BIO241": "crs_sp3.json",
    "BIO491": "crs sp4.json",
    "FNU121": "crs sp6.json",
    "FNU471": "crs sp5.json",
    "MET450": "crs sp-elec.json",
    "MET491": "crs sp11.json",    
    "FNU451": "crs sp7.json",
    "BIO444": "crs sp8.json",
}

# --- إدخال المستخدم ---
department = input("Enter Department (STAT / PHYS / BIO / FNU / MET): ").strip().upper()
code = input("Enter Course Code (110 / 241 / 491 / 121 / 471 / 444/ 450 / 451) [Optional]: ").strip()


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

# --- عرض مخرجات التعلم وطرق التقييم ---
for key in target_keys:
    json_file = course_files[key]

    try:
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)

        sections_b = data["Sections"]["B"]

        print(f"\n📘 Course Learning Outcomes and Assessment Methods for {key}:\n")
        found = False

        for outcomes_list in sections_b.values():
            if not outcomes_list:
                continue
            for outcome in outcomes_list:
                clo = outcome.get("Course Learning Outcome", "").strip()
                assessment = outcome.get("Assessment Methods", "").strip()
                if clo:
                    print(f"➤ Outcome: {clo}")
                    print(f"  Assessed by: {assessment}\n")
                    found = True

        if not found:
            print("⚠️ No learning outcomes found.")

    except Exception as e:
        print(f"❌ Error in {json_file}: {e}")
