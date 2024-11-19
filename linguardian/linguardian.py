from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageFilter
import time
from typing import List

class Linguardian:
    def __init__(self, pdf_path: str, output_pdf_path: str ):

        list_of_blurred_words = [] 
        self.pdf_path = pdf_path
        self.output_pdf_path = output_pdf_path
        self.list_of_blurred_words = list_of_blurred_words


    def extract_text_from_image(self, image):
        """Extract text and word positions from an image."""
        return pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang='jpn+eng')

    def blur_english_words(self, image, ocr_data):
        """Blur out English words in the image."""
        for j, word in enumerate(ocr_data['text']):
            if word.strip():  # Skip empty words
                # Check if the word is in English (ASCII alphabet)
                if all(char.isascii() and char.isalpha() for char in word):
                    self.list_of_blurred_words.append(word)

                    # Get the bounding box of the word
                    x, y, w, h = ocr_data['left'][j], ocr_data['top'][j], ocr_data['width'][j], ocr_data['height'][j]
                    
                    # Blur the area containing the English word
                    word_image = image.crop((x, y, x + w, y + h))
                    blurred_word_image = word_image.filter(ImageFilter.GaussianBlur(radius=5))
                    image.paste(blurred_word_image, (x, y))
        return image

    def save_image(self, image, page_num):
        """Save the image with blurred English words."""
        image.save(f"{self.output_pdf_path}_page_{page_num + 1}.png")

    def process_pdf(self):
        """Process the PDF by extracting text, blurring English words, and saving the images."""
        start_time= time.time()
        images = convert_from_path(self.pdf_path)

        for i, image in enumerate(images):
            
            ocr_data = self.extract_text_from_image(image)

            
            blurred_image = self.blur_english_words(image, ocr_data)

         
            self.save_image(blurred_image, i)

        end_time=time.time()
        time_elapsed= end_time-start_time


        print(f"Blurred images saved as {self.output_pdf_path}_page_X.png")
        print(f"Time taken: {time_elapsed} for {len(images)} pages")
        # print("\n".join(word for word in self.list_of_blurred_words))

        return images

    