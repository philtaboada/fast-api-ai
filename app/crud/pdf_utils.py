import os
from fastapi import UploadFile
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\exede\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, '../../uploads')
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

last_uploaded_file = None

def save_pdf(file: UploadFile):
    global last_uploaded_file
    pdf_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(pdf_path, 'wb') as f:
        f.write(file.file.read())
    last_uploaded_file = file.filename
    return pdf_path

def convert_pdf_to_image():
    global last_uploaded_file
    if not last_uploaded_file:
        raise ValueError("No PDF file has been uploaded yet.")
    
    pdf_path = os.path.join(UPLOAD_DIR, last_uploaded_file)
    pdf_document = fitz.open(pdf_path)
    
    image_paths = []
    for i in range(len(pdf_document)):
        page = pdf_document.load_page(i)
        image_path = pdf_path.replace('.pdf', f'_{i}.jpg')
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(image_path, 'JPEG')
        image_paths.append(image_path)
    
    pdf_document.close()
    
    return image_paths

def ocr_images():
    global last_uploaded_file
    if not last_uploaded_file:
        raise ValueError("No PDF file has been uploaded yet.")
    
    image_paths = [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR) if f.startswith(last_uploaded_file.replace('.pdf', '')) and f.endswith('.jpg')]
    
    ocr_results = {}
    for image_path in image_paths:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        ocr_results[image_path] = text
    
    return ocr_results