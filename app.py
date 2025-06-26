from flask import Flask, render_template, request
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
        return render_template("index.html", result="❌ لم يتم رفع أي ملف.")

    # ✅ التحقق من نوع الملف المدعوم
    if file_type not in ['Experience', 'Course']:
        return render_template("index.html", result="❌ نوع الملف غير مدعوم. الرجاء اختيار 'Course' أو 'Experience'.")

    try:
        for uploaded_file in uploaded_files:
            # ⏳ حفظ الملف مؤقتاً
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                uploaded_file.save(tmp.name)

            # 🧠 استخراج البيانات حسب النوع
            if file_type == 'Experience':
                json_data = extract_to_json(tmp.name)
                collection_name = "field_experience"
            elif file_type == 'Course':
                json_data = extract_course_to_json(tmp.name)
                collection_name = "course_specification"

            # 🔄 رفع البيانات إلى Firestore
            db.collection(collection_name).add({
                "file_name": uploaded_file.filename,
                "file_type": file_type,
                "data": json_data
            })

        return render_template("index.html", result="✅ Files uploaded successfully.", result_class="success")


    except Exception as e:
        return render_template("index.html", result=f"⚠️ An error occurred during processing", result_class="error")



# ✅ تشغيل الخادم
if __name__ == '__main__':
    app.run(debug=True)
