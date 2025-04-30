import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    try:
        with fitz.open(file_path) as doc:
            return " ".join([page.get_text() for page in doc])
    except Exception as e:
        print("Error reading PDF:", e)
        return ""
