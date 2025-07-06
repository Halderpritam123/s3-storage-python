import os

from .excel_reader import read_excel_file
from .csv_reader import read_csv_file
from .image_reader import read_image_file
from .text_reader import read_text_file
from .pdf_reader import read_pdf_file
from .generic_reader import fallback_reader

def read_file_by_type(file_key, file_stream, page, limit):
    extension = os.path.splitext(file_key)[1].lower()

    if extension in ['.xlsx', '.xls']:
        return read_excel_file(file_stream, page, limit)
    elif extension in ['.csv', '.tsv']:
        return read_csv_file(file_stream, page, limit)
    elif extension in ['.png', '.jpg', '.jpeg', '.gif']:
        return read_image_file(file_stream)
    elif extension in ['.txt', '.log']:
        return read_text_file(file_stream, page, limit)
    elif extension in ['.pdf']:
        return read_pdf_file(file_stream, page, limit)
    else:
        return fallback_reader(file_key)
