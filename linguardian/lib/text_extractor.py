import argparse
import time
from pdf2image import convert_from_path
import pytesseract
import os
import string


def count_language_specific_words(text):
    jap_count = 0
    eng_count = 0

    for char in text:
        
        if '\u4e00' <= char <= '\u9fff' or '\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff':
            jap_count += 1
       
        elif char.isalpha() and char.isascii():
            eng_count += 1

    return jap_count, eng_count

def count_total_words(text):
    
    exclude_punctuation = string.punctuation
    words = text.split()
    total_words = sum(1 for word in words if not all(char in exclude_punctuation for char in word))
    
    return total_words

def extract_text_from_pdf(pdf_path, output_text_file):
    """Convert PDF to images and extract text using OCR."""
    
    images = convert_from_path(pdf_path)

    # Open the output file to write OCR results

    with open(output_text_file, 'w', encoding='utf-8') as output_file:
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='jpn')
            jap_words, eng_words = count_language_specific_words(text)
           

            print(f"Page {i+1}: Japanese Words = {jap_words}, English Words = {eng_words}")

            output_file.write(f"Page {i+1}:\n")
        
            output_file.write(text)
            output_file.write("\n\n")

    print(f"OCR text extracted and saved to {output_text_file}")
