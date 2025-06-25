import os
import json
from tkinter import Tk, filedialog
from info import extract_course_info_from_docx
from Crs_Section_C import extract_course_topics_from_docx
from Crs_Section_D import extract_section_d, extract_text_from_docx as d_text
from Crs_Section_E import extract_section_e_from_docx
from Crs_Section_F_G import extract_F_and_G
from Crs_Section_A import extract_section_a_and_info
from crsSectionB import extract_clos

def browse_file(title, filetypes):
    root = Tk()
    root.withdraw()  # Hide main window
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return file_path

def browse_output_file():
    root = Tk()
    root.withdraw()
    output_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="Save output JSON file"
    )
    root.destroy()
    return output_path

def main():
   
    
    print("📝 Select course specification Word (DOCX) file:")
    docx_path = browse_file("Select DOCX File", [("Word files", "*.docx")])
    
    print("💾 Choose where to save the JSON output:")
    output_path = browse_output_file()

    if not docx_path or not output_path:

        print("❌ One or more files were not selected. Exiting.")
        return

    # Run Section A + Course Info (from PDF)
    # Get "Course Info" part from improved extractor
    course_info = extract_course_info_from_docx(docx_path)

    # Get rest of Section A content from the older method
    section_a_structure = extract_section_a_and_info(docx_path)

    # Inject the course_info into the final structure
    section_a_structure["Course Info"] = course_info
    section_a_data = section_a_structure
   


    # Run Section B (from Word)
    section_b_data = extract_clos(docx_path)

    # Run Section C (topics)
    section_c_data = extract_course_topics_from_docx(docx_path)

    # Run Section D
    doc_d, text_d = d_text(docx_path)
    section_d_data = extract_section_d(doc_d, text_d)

    # Run Section E
    section_e_data = extract_section_e_from_docx(docx_path)

    # Run Section F + G
    section_fg_data = extract_F_and_G(docx_path)

    # Combine all
    full_data = section_a_data
    full_data["Sections"]["B"] = section_b_data
    full_data["Sections"]["C"] = {"title": "Course Content (Topics)", "content": section_c_data}
    full_data["Sections"]["D"] = {"title": "Student Assessment", "content": section_d_data["Student Assessment"]}
    full_data["Sections"]["E"] = {"title": "Learning Resources and Facilities", "content": section_e_data}
    full_data["Sections"]["F"] = {
        "title": "Assessment of Course Quality",
        "content": section_fg_data["Assessment of Course Quality"]
    }
    full_data["Sections"]["G"] = {
        "title": "Specification Approval",
        "content": section_fg_data["Specification Approval"]
    }

    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=2, ensure_ascii=False)

    print("✅ Full course specification saved to:", output_path)

if __name__ == "__main__":
    main()
