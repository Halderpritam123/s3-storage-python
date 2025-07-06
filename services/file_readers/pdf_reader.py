import pdfplumber
from io import BytesIO

def read_pdf_file(file_stream, page, limit):
    buffer = BytesIO(file_stream.read())

    try:
        with pdfplumber.open(buffer) as pdf:
            total = len(pdf.pages)

            start = (page - 1) * limit
            end = min(start + limit, total)

            extracted_pages = []
            for i in range(start, end):
                page_obj = pdf.pages[i]
                text = page_obj.extract_text()
                extracted_pages.append({
                    "page_number": i + 1,
                    "text": text.strip() if text else "(No extractable text)"
                })

        return {
            "file_type": "pdf",
            "reader": "pdfplumber",
            "page": page,
            "limit": limit,
            "total_pages": total,
            "data": extracted_pages
        }

    except Exception as e:
        return {
            "error": "Failed to read PDF",
            "details": str(e)
        }
