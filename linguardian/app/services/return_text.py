import os
from uuid import uuid4
import logging
from fastapi import HTTPException
from linguardian import Linguardian
from .utils import save_file_temporarily, clean_up
from models.models import ProcessedPDF, PostProcessPDFPage, BlurMapping, AllMapping
import json

# Initialize the logger
logger = logging.getLogger(__name__)

async def return_text(file, session):
    """
    Orchestrates the entire PDF processing workflow.
    - Saves the uploaded file temporarily.
    - Uses Linguardian to process the PDF.
    - Saves results (images and blur data) to the database.
    """
    unique_filename = f"{uuid4().hex}.pdf"
    temp_pdf_path = save_file_temporarily(file, unique_filename)

    pre_process_images_dir = f"/Users/simarmalhotra/Desktop/projects/romaji-redacter/linguardian/app/data/images/pre_process_images{uuid4().hex}/"
    post_process_images_dir = f"/Users/simarmalhotra/Desktop/projects/romaji-redacter/linguardian/app/data/images/post_process_images{uuid4().hex}/"

    os.makedirs(pre_process_images_dir, exist_ok=True)
    os.makedirs(post_process_images_dir, exist_ok=True)

    try:
        # Instantiate Linguardian
        linguardian = Linguardian(temp_pdf_path, post_process_images_dir, session)

        # Process the PDF using Linguardian (if synchronous, remove await)
        output_images_data, all_ocr_data = linguardian.process_pdf()

        for page_data in all_ocr_data:
            
            data = []

            # Collect the coordinates and words for sorting
            for mapping in page_data:
                bounding_box = mapping["coordinates"]
                original_word = mapping["word"]
                data.append((bounding_box, original_word))


        
        return data 
    
        #     # Sort the data first by the y-coordinate, then by the x-coordinate
        #     sorted_data = sorted(data, key=lambda x: (x[0][1], x[0][0]))

        #     # Extract the sorted text
        #     sorted_text = " ".join([item[1] for item in sorted_data])


        #     print(f"Sorted text: {sorted_text}")
        

        

        # return {"text":sorted_text }

    except Exception as e:
        logger.error(f"Error during PDF processing: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing PDF.")

    finally:
        clean_up(temp_pdf_path)
