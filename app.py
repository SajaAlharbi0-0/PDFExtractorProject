from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, get_flashed_messages
import tempfile
import firebase_admin
from firebase_admin import credentials, firestore
from exp_Q import (
    load_location_chart,
    load_clo_group_chart,
    load_stakeholders_chart,
    load_evaluation_chart
)

import json
from firebase_config import db


# استيراد دوال التحويل
from exp1 import extract_to_json  # ملف التدريب الميداني
from crs import extract_course_to_json  # ملف توصيف المقرر

app = Flask(__name__)
app.secret_key = 'rakn_eduSpec_2025'




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
        flash("❌ No file was uploaded.", "error")
        return redirect(url_for('index') + '#upload')

    # ✅ التحقق من نوع الملف المدعوم
    if file_type not in ['Experience', 'Course']:
        flash("❌ Unsupported file type. Please choose 'Course' or 'Experience'.", "error")
        return redirect(url_for('index') + '#upload')

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
        flash(success_message, "success")
        return redirect(url_for('index') + '#upload')

    except Exception as e:
        flash("⚠️ An error occurred during processing.", "error")
        return redirect(url_for('index') + '#upload')



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
    

@app.route("/get_charts_data", methods=["POST"])
def get_charts_data():
    try:
        req = request.get_json()
        file_type = req.get("fileType")
        department = req.get("department")
        subject_code = req.get("subjectCode", "").strip()
        chart_type = req.get("chartType")
        view_type = req.get("viewType", "").strip().lower()

        if not department:
            return jsonify({"status": "error", "message": "Missing department"})

        if file_type == "Experience":
            if chart_type == "location":
                result = load_location_chart(department, subject_code)
            elif chart_type == "clo_group":
                result = load_clo_group_chart(department, subject_code)
            elif chart_type == "stakeholders":
                result = load_stakeholders_chart(department, subject_code)
            elif chart_type == "evaluation":
                result = load_evaluation_chart(department, subject_code)
                print("=== DEBUG: Evaluation Chart Result ===")
                print(result)
            else:
                return jsonify({"status": "error", "message": "Chart type not supported for Experience."})

            # 🔁 سواء طلب عرض نصي أو شارت، نتحقق من المحتوى
            if view_type == "table":
                return jsonify({
                    "status": "success",
                    "html": result.get("html", ""),
                    "data": {  # عشان ما يصير خطأ في JS
                        "labels": [],
                        "values": []
                    },
                    "isSingleCourse": result.get("isSingleCourse", False),
                    "chartTitle": result.get("chartTitle", "")
                })
            else:  # chart
                return jsonify({
                    "status": "success",
                    "data": result.get("data", {  # يدعم النتائج العادية
                        "labels": [],
                        "values": []
                    }),
                    "isSingleCourse": result.get("isSingleCourse", False),
                    "chartTitle": result.get("chartTitle", "")
                })

        else:
            return jsonify({"status": "error", "message": "Only Experience charts are supported."})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



# ✅ تشغيل الخادم
if __name__ == '__main__':
    app.run(debug=True)





















# ✅ تشغيل الخادم
if __name__ == '__main__':
    app.run(debug=True)