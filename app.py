from flask import Flask, render_template, request
from docx import Document
import re
import tempfile

app = Flask(__name__)

def clean(text):
    return re.sub(r"\s+", " ", text.replace("\xa0", " ").replace("\n", " ")).strip()

def extract_text_from_docx(doc):
    paragraphs_text = "\n".join([clean(p.text) for p in doc.paragraphs])
    tables_text = ""
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                tables_text += clean(cell.text) + "\n"
    return paragraphs_text + "\n" + tables_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('docx_files')
    search_query = request.form['search_term'].strip().lower()

    if not uploaded_files or len(uploaded_files) == 0:
        return render_template("index.html", result="❌ لم يتم رفع أي ملف.")

    results = []

    for uploaded_file in uploaded_files:
        # حفظ الملف مؤقتًا
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            uploaded_file.save(tmp.name)
            doc = Document(tmp.name)

        full_text = extract_text_from_docx(doc)
        lines = full_text.splitlines()

        # دعم البحث المتقدم: البحث عن وجود كل كلمة من الاستعلام (AND بين الكلمات)
        query_words = search_query.split()
        matched_lines = []
        for line in lines:
            line_lower = line.lower()
            if all(word in line_lower for word in query_words):
                matched_lines.append(line)

        if matched_lines:
            results.append({
                "filename": uploaded_file.filename,
                "matches": matched_lines
            })

    if not results:
        return render_template("index.html", result="❌ لم يتم العثور على نتائج مطابقة.")

    return render_template("index.html", results=results, query=search_query)

if __name__ == '__main__':
    app.run(debug=True)