import os
import fitz  # PyMuPDF

def extract_pages(input_pdf, pages_to_extract=5, start_page=30):
    """Extract a specified number of pages from a PDF."""
    

    doc = fitz.open(input_pdf)
    new_doc = fitz.open()
    
    end_page = min(start_page + pages_to_extract, doc.page_count)
    for page_num in range(start_page, end_page):
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    

    output_dir = "pdfs"
    os.makedirs(output_dir, exist_ok=True)
    
    
    output_pdf = f"{output_dir}/{pages_to_extract}_pages_from_{start_page}.pdf"
    
    # Save the extracted pages to the new PDF file
    new_doc.save(output_pdf)
    new_doc.close()
    doc.close()
    
    print(f"Successfully saved {end_page - start_page} pages to '{output_pdf}'")

# Example usage:
extract_pages("pdfs/full-genki.pdf", pages_to_extract=5, start_page=50)
