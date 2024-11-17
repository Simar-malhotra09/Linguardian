import fitz  # PyMuPDF
import re
import unicodedata
import argparse
import os

import time



class Redactor:
    def __init__(self, path):
        self.path = path

    def is_english_word(self, word):
        """Check if the word contains only Latin characters."""
        for char in word:
            # Check if the character is Latin or a common punctuation mark
            if not ('LATIN' in unicodedata.name(char, '') or char in ".,!?"):
                return False
        return True

    def redaction(self):
        """Redact English words from the PDF."""
        doc = fitz.open(self.path)
        start_time = time.time() 

        # Iterate through each page
        for page in doc:
            page.wrap_contents()  # Fix alignment issues

            # Extract text using a method that retains control characters
            lines = page.get_text("text-with-control").splitlines()

            for line in lines:
                words = line.split()
                for word in words:
                    if self.is_english_word(word):
                        # Locate the position of each detected word on the page
                        areas = page.search_for(word)
                        # Add redaction annotations (fill with black color)
                        for area in areas:
                            page.add_redact_annot(area, fill=(0, 0, 0))
            
 
            page.apply_redactions()
        file_name = os.path.basename(self.path)
        output_path = f"pdfs/redacted/redacted_{file_name}"
        doc.save(output_path)

        end_time= time.time()

        time_elapsed = end_time-start_time

        print(f"Successfully redacted English text in {time_elapsed}s. Saved as '{output_path}'.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Redact English words from a PDF.")
    parser.add_argument('--file', type=str, required=True, help='Path to the input PDF file')
    args = parser.parse_args()


    redactor = Redactor(args.file)
    redactor.redaction()
