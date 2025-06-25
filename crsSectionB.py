from docx import Document
import json
import re

def extract_clos(doc_path):
    clos_data = {
        "1.0 Knowledge and understanding": [],
        "2.0 Skills": [],
        "3.0 Values, autonomy, and responsibility": []
    }

    doc = Document(doc_path)
    target_table = None

    expected_headers = [
        "Code",
        "Course Learning Outcomes",
        "Code of CLOs aligned with program",
        "Teaching Strategies",
        "Assessment Methods"
    ]

    for tbl in doc.tables:
        hdr = [c.text.replace("\n", " ").strip() for c in tbl.rows[0].cells]
        # code to delete \n from hdr = Table headers detected: ['code', 'course learning\noutcomes', 'code of clos aligned\nwith program', 'teaching\nstrategies', 'assessment\nmethods']


        print("Table headers detected:", hdr)  # 🐞 Debug output
        if hdr[:5] == expected_headers:
            target_table = tbl
            break

    if not target_table:
        print(hdr)
        raise RuntimeError("Couldn't find the CLOs table.")

    code_pattern = re.compile(r"^[1-3]\.(?!0$)\d+")

    for row in target_table.rows:
        cells = row.cells
        if len(cells) < 5:
            continue

        code = cells[0].text.strip()
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

    return clos_data
