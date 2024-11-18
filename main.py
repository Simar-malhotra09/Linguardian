import fitz  # PyMuPDF
import pymupdf4llm
import re
import unicodedata
import argparse
import os

import time

'''This approach wont work (Im so dumb) since it's a scanned version and no text is encoded in the first place'''


class Redactor:
    def __init__(self, path, total_redcs=0):
        self.path = path
        self.total_redcs=total_redcs





    def is_english_word(self, word):
        """Check if the first char word contains Latin characters."""
        if not word:
            return False
        
        print(f"Checking word: {word}")
        if ('LATIN' in unicodedata.name(word[0], '') or word[0] in ".,!?"):
            return True
        
        
        return False

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
                        self.total_redcs+=1
                        # Locate the position of each detected word on the page
                        areas = page.search_for(word)

                        # Add redaction annotations (fill with black color)
                        for area in areas:
                            page.add_redact_annot(area, fill=(0, 0, 0))
            
 
            page.apply_redactions()
        file_name = os.path.basename(self.path)
        output_path = f"pdfs/redacted/redacted_{file_name}"
        doc.save(output_path, garbage=4, deflate=True)

        end_time= time.time()

        time_elapsed = end_time-start_time

        print(f"Successfully redacted English text in {time_elapsed}s. Saved as '{output_path}'. Redacted {self.total_redcs} words")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redact English words from a PDF.")

    parser.add_argument('--file', type=str, required=True, help='Path to the input PDF file')
    args = parser.parse_args()


    md_text = pymupdf4llm.to_markdown(args.file)
    output_file = "output.md"  
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_text)
    print(f"Markdown content has been written to '{output_file}'")


    # redactor = Redactor(args.file)
    # redactor.redaction()
