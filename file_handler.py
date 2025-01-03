# file_handler.py
import os
import pdfplumber
from docx import Document

def extract_data_from_file(file_path):
    """
    Extract data from a file based on its extension.
    :param file_path: Path to the file.
    :return: Extracted text from the file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_data_from_pdf(file_path)
    elif ext == ".txt":
        return extract_data_from_txt(file_path)
    elif ext in [".doc", ".docx"]:
        return extract_data_from_doc(file_path)
    else:
        return "Unsupported file type."

def extract_data_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''.join([page.extract_text() for page in pdf.pages])
    return text

def extract_data_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_data_from_doc(file_path):
    doc = Document(file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
