
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from linguardian.linguardian import Linguardian
import shutil
from uuid import uuid4

app = FastAPI()

output_dir = 'pdfs/fast'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


'''create a temp local copy of the pdf,
    apply processes and for now return the 
    images in a zip folder.
'''
@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...)):

    # Generate a unique filename for the uploaded PDF
    unique_filename = f"temp_{uuid4().hex}.pdf"
    
    # Save the uploaded file temporarily
    with open(unique_filename, "wb") as f:
        f.write(await file.read())
    
    try:
        # Process the PDF and get the output images
        blurrer = Linguardian(unique_filename, "pdfs/fast")
        output_images = blurrer.process_pdf()

        # If it's a single image, return it directly
        if isinstance(output_images, list):
            
            output_zip_path = f"pdfs/fast/{unique_filename}.zip"
            shutil.make_archive(output_zip_path, 'zip', 'pdfs/fast', unique_filename)

            
            return FileResponse(output_zip_path, media_type="application/zip")
        else:
        
            return FileResponse(output_images, media_type="image/png")
    
    finally:
        # delete the temp file
        os.remove(unique_filename)


