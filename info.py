from docx import Document

def extract_course_info_from_docx(doc_path):
    doc = Document(doc_path)

    course_info = {
        "Course Title": "",
        "Course Code": "",
        "Program": "",
        "Department": "",
        "Faculty": "",
        "University": "",
        "Version": "",
        "Last Revision Date": ""
    }

    expected_labels = {
        "course title": "Course Title",
        "title": "Course Title",
        "course code": "Course Code",
        "code": "Course Code",
        "program": "Program",
        "department": "Department",
        "faculty": "Faculty",
        "college": "Faculty",
        "institution": "University",
        "university": "University",
        "version": "Version",
        "last revision date": "Last Revision Date",
        "revision date": "Last Revision Date"
    }

    already_filled = set()

    for table in doc.tables:
        for row in table.rows:
            cells = row.cells
            if len(cells) == 2:
                label = cells[0].text.strip().lower()
                value = cells[1].text.strip()
                for key, field in expected_labels.items():
                    if key in label and field not in already_filled:
                        course_info[field] = value
                        already_filled.add(field)
            elif len(cells) == 1:
                text = cells[0].text.strip()
                if ":" in text:
                    label, value = text.split(":", 1)
                    label = label.strip().lower()
                    value = value.strip()
                    for key, field in expected_labels.items():
                        if key in label and field not in already_filled:
                            course_info[field] = value
                            already_filled.add(field)

    return course_info
