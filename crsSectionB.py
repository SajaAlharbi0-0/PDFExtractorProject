from docx import Document
import json
import re

# 1. Full file and output
doc_path         = "C:/Users/sajaa/Downloads/crs_spfinal.docx"
output_json_path = "C:/Users/sajaa/Downloads/clos_only_output.json"

# 2. Prepare JSON buckets
clos_data = {
    "1.0 Knowledge and understanding": [],
    "2.0 Skills": [],
    "3.0 Values, autonomy, and responsibility": []
}

# 3. Load and find the Section B table by its header row
doc = Document(doc_path)
target_table = None
for tbl in doc.tables:
    hdr = [c.text.strip() for c in tbl.rows[0].cells]
    if hdr[:5] == [
        "Code",
        "Course Learning Outcomes",
        "Code of Aligned PLOs",
        "Teaching Strategies",
        "Assessment Methods"
    ]:
        target_table = tbl
        break
if not target_table:
    raise RuntimeError("Couldn't find the CLOs table.")

# 4. Only capture codes that are NOT the section headers (i.e. skip *.0)
#    This regex matches 1.x, 2.x, 3.x where x ≠ 0
code_pattern = re.compile(r"^[1-3]\.(?!0$)\d+")

for row in target_table.rows:
    cells = row.cells
    if len(cells) < 5:
        continue

    code = cells[0].text.strip()
    # skip headers 1.0, 2.0, 3.0 (and any non-CLO rows)
    if not code_pattern.match(code):
        continue

    outcome    = " ".join(cells[1].text.split())
    plo        = " ".join(cells[2].text.split())
    strategy   = " ".join(cells[3].text.split())
    assessment = " ".join(cells[4].text.split())

    group_key = {
        "1": "1.0 Knowledge and understanding",
        "2": "2.0 Skills",
        "3": "3.0 Values, autonomy, and responsibility"
    }[code[0]]

    clos_data[group_key].append({
        "Code": code,
        "Course Learning Outcome": outcome,
        "PLO Code": plo,
        "Teaching Strategies": strategy,
        "Assessment Methods": assessment
    })

# 5. Write JSON
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(clos_data, f, ensure_ascii=False, indent=2)

print("✅ Extracted only true CLOs (skipped 1.0, 2.0, 3.0 headers).")
