# field_parser.py
import fitz  # PyMuPDF ➜ pip install pymupdf
import re
import json
from pathlib import Path
from tkinter import Tk, filedialog

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
    return {
        "Credit Hours": _grab(r"Credit\s*hours.*?\(\s*(\d+)\s*credit", text),
        "Level/Year"  : _grab(r"Level\/year.*?offered:\s*(.*?)\n", text),
        "Duration": {
            "Weeks" : int(convert_arabic_digits(_grab(r"\(\s*([\d٠-٩]+)\s*\)\s*Weeks",  text, "0"))),
            "Days"  : int(convert_arabic_digits(_grab(r"Weeks.*?\(\s*([\d٠-٩]+)\s*\)\s*Days",  text, "0"))),
            "Hours" : int(convert_arabic_digits(_grab(r"Days.*?\(\s*([\d٠-٩]+)\s*\)\s*Hours", text, "0"))),
        },
        "Corequisite": _grab([
            r"Corequisite.*?\n\s*(.*?)\n",
            r"Corequisite.*?:\s*(.*?)\n"
        ], text, ""),
        "Delivery Mode": {
            "In-person": bool(re.search(r"[☒Xx]\s*In[- ]?person", text, re.IGNORECASE)),
            "Hybrid"   : bool(re.search(r"[☒Xx]\s*Hybrid",      text, re.IGNORECASE)),
            "Online"   : bool(re.search(r"[☒Xx]\s*Online",      text, re.IGNORECASE)),
        }
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
        "Field Experience Details": extract_field_experience_details(text)
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
