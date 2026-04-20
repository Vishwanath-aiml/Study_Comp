import fitz  # PyMuPDF
import io

def extract_text_from_pdf(drive_service, file_id):
    request = drive_service.files().get_media(fileId=file_id)
    pdf_bytes = request.execute()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text