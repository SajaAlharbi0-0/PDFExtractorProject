from flask import Flask, render_template, request, jsonify
import tempfile
import firebase_admin
from firebase_admin import credentials, firestore

# استيراد دوال التحويل
from exp1 import extract_to_json  # ملف التدريب الميداني
from crs import extract_course_to_json  # ملف توصيف المقرر

app = Flask(__name__)

# 🔐 إعداد Firebase
cred = credentials.Certificate("secrets/firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 🏠 الصفحة الرئيسية
@app.route('/')
def index():
    return render_template("index.html")  # ✅ يعرض الواجهة

# 📤 رفع الملف ومعالجته
@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('docx_files')
    file_type = request.form.get('file_type', '').strip()

    # ✅ التحقق من رفع الملفات
    if not uploaded_files:
        return render_template("index.html", result="❌ No file was uploaded.", result_class="error")

    # ✅ التحقق من نوع الملف المدعوم
    if file_type not in ['Experience', 'Course']:
        return render_template("index.html", result="❌ Unsupported file type. Please choose 'Course' or 'Experience'.", result_class="error")

    try:
        uploaded_names = []

        for uploaded_file in uploaded_files:
            # ⏳ حفظ الملف مؤقتاً
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                uploaded_file.save(tmp.name)
                temp_path = tmp.name  # نحتفظ بالمسار المؤقت

            # 🧠 استخراج البيانات حسب النوع
            if file_type == 'Experience':
                json_data = extract_to_json(temp_path)
                collection_name = "field_experience"
            elif file_type == 'Course':
                json_data = extract_course_to_json(temp_path)
                collection_name = "course_specification"

            # 🔄 رفع البيانات إلى Firestore
            db.collection(collection_name).add({
                "file_name": uploaded_file.filename,
                "file_type": file_type,
                "data": json_data
            })

            uploaded_names.append(uploaded_file.filename)

        success_message = f"✅ Files uploaded successfully: {', '.join(uploaded_names)}"
        return render_template("index.html", result=success_message, result_class="success")

    except Exception as e:
        return render_template("index.html", result="⚠️ An error occurred during processing.", result_class="error")


# ✅ إرجاع قائمة الأقسام (BIO, FNU...) حسب نوع الملف
@app.route('/get_departments', methods=['POST'])
def get_departments():
    import re  # ⬅️ ضيف المكتبة هنا أو في بداية الملف
    data = request.get_json()
    file_type = data.get('fileType', '')
    file_type_lower = file_type.lower()

    if file_type_lower not in ['experience', 'course']:
        return jsonify({"status": "error", "message": "Invalid file type"}), 400

    collection_name = "field_experience" if file_type_lower == "experience" else "course_specification"

    try:
        docs = db.collection(collection_name).stream()
        departments = set()

        for doc in docs:
            doc_data = doc.to_dict()
            course_code = ""

            if file_type == "Experience":
                course_code = doc_data["data"].get("General Info", {}).get("Course Code", "")
            elif file_type == "Course":
                course_code = doc_data["data"].get("Course Info", {}).get("Course Code", "")

            # استخراج الأحرف الأولى فقط مثل BIO من BIO390 أو Bio 491
            if course_code:
                match = re.match(r'^([A-Za-z]+)', course_code.strip())
                if match:
                    departments.add(match.group(1).upper())

        return jsonify({
            "status": "success",
            "departments": sorted(list(departments))
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500































# ✅ تشغيل الخادم
if __name__ == '__main__':
    app.run(debug=True)

