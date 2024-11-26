# app/linguardian.py
import time
from typing import List
from PIL import Image, ImageFilter
import pytesseract
from pdf2image import convert_from_path
from io import BytesIO
from models.models import *
from sqlalchemy.orm import Session

class Linguardian:
    def __init__(self, file_path: str, post_process_images: str, db: Session):
        self.file_path = file_path  
        self.post_process_images = post_process_images
        self.list_of_blurred_words = []
        self.db = db

    def extract_text_from_image(self, image):
        """Extract text and word positions from an image."""
        return pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang='jpn+eng')

    def blur_english_words(self, image, ocr_data):
        """Blur out English words in the image."""
        all_blurred_words_and_bbox = []
        for j, word in enumerate(ocr_data['text']):
            if word.strip():
                print(f"Word: {word}, Coordinates: ({ocr_data['left'][j]}, {ocr_data['top'][j]}, {ocr_data['width'][j]}, {ocr_data['height'][j]})")
                if all(char.isascii() and char.isalpha() for char in word):
                    self.list_of_blurred_words.append(word)

                    # Get the bounding box of the word
                    x, y, w, h = ocr_data['left'][j], ocr_data['top'][j], ocr_data['width'][j], ocr_data['height'][j]

                    all_blurred_words_and_bbox.append({
                        "word": word,
                        "coordinates": (x, y, x + w, y + h)
                    })

                    # Blur the area containing the English word
                    word_image = image.crop((x, y, x + w, y + h))
                    blurred_word_image = word_image.filter(ImageFilter.GaussianBlur(radius=5))
                    image.paste(blurred_word_image, (x, y))
        return image, all_blurred_words_and_bbox

    def save_image(self, image, page_num):
        """Save the image with blurred English words."""
        image_path = f"{self.post_process_images}_page_{page_num + 1}.png"
        image.save(image_path)
        return image_path
    


    def process_pdf(self):
        """Process the PDF by extracting text, blurring English words, and saving the images."""
        start_time = time.time()
       


        images = convert_from_path(self.file_path)

        output_data = []

        for i, image in enumerate(images):
            ocr_data = self.extract_text_from_image(image)
            blurred_image, all_blurred_words_and_bbox = self.blur_english_words(image, ocr_data)
            image_path = self.save_image(blurred_image, i)

            output_data.append({
                "image_path": image_path,
                "blurred_words_and_bbox": all_blurred_words_and_bbox
            })

        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f"Blurred images saved as {self.post_process_images}_page_X.png")
        print(f"Time taken: {time_elapsed} for {len(images)} pages")
        
        return output_data
