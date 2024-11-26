import os
import fitz  # PyMuPDF
import string
from pdf2image import convert_from_path
import pytesseract
from uuid import uuid4
from typing import List

def save_file_temporarily(file, unique_filename: str) -> str:
    """
    Save the uploaded file temporarily.
    Args:
        file: The file object to be saved.
        unique_filename (str): The unique filename for saving.
    Returns:
        str: The file path where the file is saved temporarily.
    """
    temp_pdf_path = f"/Users/simarmalhotra/Desktop/projects/romaji-redacter/linguardian/app/data/pdfs/{unique_filename}"
    with open(temp_pdf_path, "wb") as f:
        f.write(file.file.read())  
    return temp_pdf_path


def clean_up(file_path: str) -> None:
    """
    Clean up (delete) a temporary file.
    Args:
        file_path (str): Path to the file to be deleted.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def extract_pages(input_pdf: str, pages_to_extract: int = 5, start_page: int = 30) -> str:
    """
    Extract a specified number of pages from a PDF and save them as a new PDF.
    Args:
        input_pdf (str): Path to the input PDF.
        pages_to_extract (int): Number of pages to extract.
        start_page (int): The starting page number to extract from.
    Returns:
        str: The path to the new PDF file containing the extracted pages.
    """
    doc = fitz.open(input_pdf)
    new_doc = fitz.open()
    
    end_page = min(start_page + pages_to_extract, doc.page_count)
    for page_num in range(start_page, end_page):
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    
    output_dir = "pdfs"
    os.makedirs(output_dir, exist_ok=True)
    output_pdf = f"{output_dir}/{pages_to_extract}_pages_from_{start_page}.pdf"
    new_doc.save(output_pdf)
    new_doc.close()
    doc.close()
    
    print(f"Successfully saved {end_page - start_page} pages to '{output_pdf}'")
    return output_pdf


def save_pdf_as_images(pdf_path: str, output_dir: str, dpi: int = 300) -> List[str]:
    """
    Convert a PDF file to images and save them in the specified directory.
    Args:
        pdf_path (str): Path to the PDF file to be converted.
        output_dir (str): Directory to save the resulting images.
        dpi (int): DPI resolution for the output images (default is 300).
    Returns:
        List[str]: A list of file paths to the saved images.
    """
    os.makedirs(output_dir, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=dpi)
    saved_image_paths = []
    
    for i, image in enumerate(images):
        output_path = os.path.join(output_dir, f"page_{i + 1}.png")
        image.save(output_path, "PNG")
        saved_image_paths.append(output_path)

    return saved_image_paths


def count_language_specific_words(text: str) -> tuple:
    """
    Count the number of Japanese and English words in a given text.
    Args:
        text (str): The text to be analyzed.
    Returns:
        tuple: A tuple containing the count of Japanese words and English words.
    """
    jap_count = 0
    eng_count = 0

    for char in text:
        if '\u4e00' <= char <= '\u9fff' or '\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff':
            jap_count += 1
        elif char.isalpha() and char.isascii():
            eng_count += 1

    return jap_count, eng_count


def count_total_words(text: str) -> int:
    """
    Count the total number of words in the text, excluding punctuation.
    Args:
        text (str): The text to be analyzed.
    Returns:
        int: The total word count.
    """
    exclude_punctuation = string.punctuation
    words = text.split()
    total_words = sum(1 for word in words if not all(char in exclude_punctuation for char in word))
    
    return total_words


def extract_text_from_pdf(pdf_path: str, output_text_file: str) -> None:
    """
    Convert a PDF to images and extract text using OCR (Tesseract).
    Args:
        pdf_path (str): The path to the PDF file to be processed.
        output_text_file (str): Path to the file where extracted text will be saved.
    """
    images = convert_from_path(pdf_path)

    with open(output_text_file, 'w', encoding='utf-8') as output_file:
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='jpn')
            jap_words, eng_words = count_language_specific_words(text)
            
            print(f"Page {i+1}: Japanese Words = {jap_words}, English Words = {eng_words}")

            output_file.write(f"Page {i+1}:\n")
            output_file.write(text)
            output_file.write("\n\n")

    print(f"OCR text extracted and saved to {output_text_file}")
