
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from linguardian.linguardian import Linguardian
import shutil
from uuid import uuid4
from datetime import datetime, timezone
import json


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models import Base,ProcessedPDF,PDFPage,BlurMapping

app = FastAPI()

engine= create_engine("sqlite:///blur_mapping.db", echo=True)
Base.metadata.create_all(bind=engine)

Session= sessionmaker(bind=engine)
session=Session()

output_dir = 'pdfs/db/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


'''create a temp local copy of the pdf,
    apply processes and for now return the 
    images in a zip folder.
'''

@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...)):
    session = Session()  # Create a database session
    unique_filename = f"temp_{uuid4().hex}.pdf"

    try:
        # Step 1: Save the uploaded PDF temporarily
        with open(unique_filename, "wb") as f:
            f.write(await file.read())

        # Step 2: Add PDF metadata to the database
        new_pdf = ProcessedPDF(file_name=file.filename ,zip_path=None)
        session.add(new_pdf)
        session.commit()

        # Step 3: Process the PDF
        blurrer = Linguardian(unique_filename, output_dir)
        output_images_data = blurrer.process_pdf()  

        #Step 4: 
        for page_number, page_data in enumerate(output_images_data, start=1):
            image_path = page_data["image_path"]
            blurred_words_and_bbox = page_data["blurred_words_and_bbox"]
            
            # Save the page record
            new_page = PDFPage(pdf_id=new_pdf.id, page_number=page_number, image_path=image_path)
            session.add(new_page)
            session.commit()  # Commit to get the new page's ID
            
            # Save the blur mappings for this page
            for mapping in blurred_words_and_bbox:  
                blur_mapping = BlurMapping(
                    page_id=new_page.id,  # Reference to the page
                    bounding_box=json.dumps(mapping["coordinates"]),  # Serialize coordinates to JSON
                    original_word=mapping["word"]  # Use "word" for original text
                )
                session.add(blur_mapping)
            
            session.commit() 


        # Step 5: Create a zip file with the processed images
        output_zip_path = f"{output_dir}/{uuid4().hex}.zip"
        shutil.make_archive(output_zip_path.rstrip(".zip"), 'zip', output_dir)

        return FileResponse(output_zip_path, media_type="application/zip")

    except Exception as e:
        print(f"Error processing PDF: {e}")
        session.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # Step 7: Clean up
        os.remove(unique_filename)
        session.close()