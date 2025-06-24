import docx
import json
#by razan
def extract_course_topics_from_docx(docx_path, output_json_path=None):
    doc = docx.Document(docx_path)
    course_content_started = False
    course_content = []
    topic_number = 1
    stop_words = ['total', 'Total']

    for table in doc.tables:
        headers = [cell.text.strip().lower() for cell in table.rows[0].cells]

        # Start if 'list of topics' found in headers
        if not course_content_started and any("list of topics" in h for h in headers):
            course_content_started = True

        if course_content_started:
            for row in table.rows[1:]:  # Skip header
                cells = row.cells
                if len(cells) >= 2:
                    topic_text = cells[1].text.strip()
                    if topic_text:
                        # Stop if 'Total' appears in the row
                        if any(stop_word in topic_text.lower() for stop_word in stop_words):
                            course_content_started = False
                            break
                        course_content.append({
                            "no": topic_number,
                            "topic": topic_text
                        })
                        topic_number += 1

    result = {"topics": course_content}

    if output_json_path:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    return result

# ✅ Usage
docx_path = "crs sp2 (1).docx"  # Change this if needed
output_json = "course_topics_from_docx.json"

data = extract_course_topics_from_docx(docx_path, output_json)
print(json.dumps(data, indent=2, ensure_ascii=False))