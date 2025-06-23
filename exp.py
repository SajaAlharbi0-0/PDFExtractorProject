import fitz  # PyMuPDF ➜ pip install pymupdf
import re
import json
from pathlib import Path
from tkinter import Tk, filedialog
import pdfplumber, re ,camelot



# ---------- تحويل الأرقام الهندية إلى إنجليزية ----------
def convert_arabic_digits(txt: str) -> str:
    arabic = "٠١٢٣٤٥٦٧٨٩"
    for i, d in enumerate(arabic):
        txt = txt.replace(d, str(i))
    return txt

# ---------- التقاط أول تطابق ----------
def _grab(patterns, text, default=None, flags=re.IGNORECASE):
    if isinstance(patterns, str):
        patterns = [patterns]
    for pat in patterns:
        m = re.search(pat, text, flags)
        if m:
            return m.group(1).strip()
    return default

# ---------- Field A ----------
def extract_field_experience_details(text: str) -> dict:
    modes = []
    if re.search(r"[☒Xx]\s*In[- ]?person", text, re.IGNORECASE):
        modes.append("In-person")
    if re.search(r"[☒Xx]\s*Hybrid", text, re.IGNORECASE):
        modes.append("Hybrid")
    if re.search(r"[☒Xx]\s*Online", text, re.IGNORECASE):
        modes.append("Online")

    return {
        "Credit Hours": _grab(r"Credit\s*hours.*?\(\s*(\d+)\s*credit", text),
        "Level/Year": _grab(r"Level\/year.*?offered:\s*(.*?)\n", text),
        "Duration": {
        "Weeks": int(convert_arabic_digits(_grab(r"\(\s*([\d٠-٩]+)\s*\)\s*Weeks", text, "0"))),
        "Days": int(convert_arabic_digits(_grab(r"\(\s*([\d٠-٩]+)\s*\)\s*Days", text, "0"))),
        "Hours": int(convert_arabic_digits(_grab(r"\(\s*([\d٠-٩]+)\s*\)\s*Hours", text, "0"))),
},

        "Corequisite": _grab([
            r"Corequisite.*?\n\s*(.*?)\n",
            r"Corequisite.*?:\s*(.*?)\n"
        ], text, ""),
        "Delivery Mode": modes
    }

# ---------- Field B ----------
def extract_clos_grouped(file_path: str) -> dict:
    import camelot

    tables = camelot.read_pdf(file_path, pages='all', flavor='stream')  # or 'lattice' if borders are clear
    print(f"✅ Found {len(tables)} tables.")

    # نفترض أن الجدول المناسب هو رقم 1 حسب اختبارك السابق
    table = tables[1].df
    clos = {}
    current_section = None

    for index, row in table.iterrows():
        # تخطى الصفوف الفارغة
        if row.isnull().all() or row[0].strip() == "":
            continue

        code = row[0].strip()

        # إذا الصف عبارة عن عنوان رئيسي (مثل 2.0 Skills)
        if re.match(r"^\d+\.0$", code):
            current_section = code
            clos[current_section] = {
                "Title": row[1].strip(),
                "Items": []
            }
            continue

        # إذا الصف عبارة عن CLO عادي
        if re.match(r"^\d+\.\d+$", code) and current_section:
            try:
                clos[current_section]["Items"].append({
                    "Code": code,
                    "Outcome": row[1].strip(),
                    "PLO Code": row[2].strip(),
                    "Activities": row[3].strip(),
                    "Assessment Methods": row[4].strip(),
                    "Responsibility": row[5].strip()
                })
            except IndexError:
                print(f"⚠️ Skipping incomplete row at index {index}: {row}")

    return clos






# ---------- Field C ----------
def extract_spec_approval_data(text: str) -> dict:
    council = _grab(r"Council\s*/Committee\s*(.*?)\n", text, "")
    reference_no = _grab(r"Reference No\.\s*(\d+)", text, "")
    date = _grab(r"Date\s*([\d/]+\s*H\s*[–-]\s*[\dA-Z\s]+)", text, "")

    return {
        "Council/Committee": council,
        "Reference No": reference_no,
        "Date": date
    }



# ---------- استخراج البيانات ----------
def extract_data(file_path):
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)

    return {
        "General Info": {
            "Course Title"      : _grab(r"Course Title:\s+(.*?)\n", text),
            "Course Code"       : _grab(r"Course Code:\s+(.*?)\n",  text),
            "Program"           : _grab(r"Program:\s+(.*?)\n",      text),
            "Department"        : _grab(r"Department:\s+(.*?)\n",   text),
            "College"           : _grab(r"College:\s+(.*?)\n",      text),
            "Institution"       : _grab(r"Institution:\s+(.*?)\n",  text),
            "Version"           : _grab(r"Field Experience Version Number:\s+(.*?)\n", text),
            "Last Revision Date": _grab(r"Last Revision Date:\s+(.*?)\n",             text),
        },
        "Field Experience Details": extract_field_experience_details(text),
        "Field Experience Course Learning Outcomes (CLOs), Training Activities and Assessment Methods":
        extract_clos_grouped(file_path),

        "Specification Approval Data": extract_spec_approval_data(text)
 

    }

# ---------- واجهة اختيار الملف ----------
def select_pdf_file():
    root = Tk()
    root.withdraw()  # إخفاء نافذة Tk
    filepath = filedialog.askopenfilename(
        title="اختر ملف PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )
    return filepath

# ---------- نقطة البداية ----------
if __name__ == "__main__":
    pdf_path = select_pdf_file()

    if not pdf_path:
        print("❌ لم يتم اختيار أي ملف.")
        exit()

    print(f"✅ جاري تحليل الملف: {pdf_path}")
    data = extract_data(pdf_path)

    # طباعة النتائج
    print("\n📋 البيانات المستخرجة:")
    for section, fields in data.items():
        print(f"\n🔹 {section}")
        for k, v in fields.items():
            print(f"{k:<25}: {v}")

    # حفظ JSON
    json_path = Path(__file__).parent / (Path(pdf_path).stem + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\n✅ تم حفظ البيانات في: {json_path}")
