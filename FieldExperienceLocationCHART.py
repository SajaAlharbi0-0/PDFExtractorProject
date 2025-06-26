import json

# --- ربط كل كورس بملفه ---
course_files = {
    "BIO390": "field_exp_sp(final)_extracted.json",
    "FNU484": "field_exp sp3_extracted.json",
     "FNU473": "field_exp sp2_extracted.json"
}

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
    target_keys = [k for k in course_files if k.startswith(department)]
    if not target_keys:
        print(f"❌ No courses found for department {department}")
        exit()

# --- استخراج وعرض أماكن التدريب ---
for key in target_keys:
    json_file = course_files[key]

    try:
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)

        locs = data["C.\tField Experience Administration"]["3. Field Experience Location Requirements"]
        unique_locations = [d["Location"] for d in locs if d["Location"].strip()]

        print(f"\n📍 Training Locations for {key}:")
        for loc in unique_locations:
            print(f" - {loc}")

    except Exception as e:
        print(f"❌ Error in {json_file}: {e}")
