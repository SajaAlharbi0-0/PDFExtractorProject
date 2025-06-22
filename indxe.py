import pdfplumber
import pandas as pd

pdf_path = "C:/Users/mahaf/Downloads/crs sp1.pdf"
excel_output = "C:/Users/mahaf/Downloads/output_data_cleaned.xlsx"

all_tables = []
text_data = []

with pdfplumber.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        if text:
            text_data.append({"Page": page_number, "Content": text.strip()})

        tables = page.extract_tables()
        if tables:
            for idx, table in enumerate(tables):
                if table:
                    df_raw = pd.DataFrame(table)

                    # عدد الأعمدة في الجدول
                    num_cols = df_raw.shape[1]

                    # توليد أسماء أعمدة افتراضية
                    col_names = [f"Column_{i+1}" for i in range(num_cols)]

                    # إذا عدد الأعمدة معروف (مثلاً 5 أو 6) نستخدم أسماء مفهومة
                    if num_cols == 5:
                        col_names = ['Code', 'Learning Outcome', 'PLO Code', 'Strategy', 'Assessment']
                    elif num_cols == 6:
                        col_names = ['Code', 'Outcome', 'PLO Code', 'Strategy', 'Assessment', 'Other']

                    df_raw.columns = col_names

                    # تنظيف النصوص من مشاكل السطور الجديدة والفراغات
                    for col in df_raw.columns:
                        df_raw[col] = df_raw[col].astype(str).str.replace('\n', ' ').str.strip()

                    all_tables.append((f"Table_Page{page_number}_{idx+1}", df_raw))

# حفظ البيانات في ملف Excel
with pd.ExcelWriter(excel_output, engine='xlsxwriter') as writer:
    if text_data:
        pd.DataFrame(text_data).to_excel(writer, sheet_name="Text_Content", index=False)

    for sheet_name, df in all_tables:
        df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

print(f"✅ Excel file created at: {excel_output}")