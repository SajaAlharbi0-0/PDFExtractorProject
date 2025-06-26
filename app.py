from flask import Flask, render_template, request
from docx import Document
import re
import tempfile
import firebase_admin
from firebase_admin import credentials, firestore
from exp1 import extract_to_json  # ⬅️ دالة تحويل ملفات التدريب فقط


app = Flask(__name__)

# 🔐 إعداد Firebase
cred = credentials.Certificate("secrets/firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 🏠 الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# 📤 رفع الملف ومعالجته
@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('docx_files')
    file_type = request.form.get('file_type')

    # ⚠️ التحقق من رفع الملفات
    if not uploaded_files:
        return render_template("index.html", result="❌ لم يتم رفع أي ملف.")

    # ⚠️ دعم نوع واحد فقط حالياً
    if file_type != 'field':
        return render_template("index.html", result="❌ حالياً فقط ملفات التدريب الميداني مدعومة.")

    try:
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                uploaded_file.save(tmp.name)

            # 🔍 استخراج وتحويل البيانات
            json_data = extract_to_json(tmp.name)

            # 🔄 رفع إلى Firestore
            db.collection("field_experience").add({
                "file_name": uploaded_file.filename,
                "file_type": file_type,
                "data": json_data
            })

        # ✅ رسالة نجاح
        return "✅ File uploaded successfully"


    except Exception as e:
        # ⚠️ في حال حصل خطأ
        return render_template("index.html", result=f"⚠️ خطأ أثناء التحويل: {str(e)}")

# ✅ تشغيل الخادم
if __name__ == '__main__':
    app.run(debug=True)