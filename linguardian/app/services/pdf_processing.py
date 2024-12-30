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

async def process_pdf(file, session):
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
        blurred_text_and_bbox, all_text_and_bbox = linguardian.process_pdf()

        # Save results to the database
        new_pdf = ProcessedPDF(file_name=file.filename, file_path=pre_process_images_dir)
        session.add(new_pdf)
        session.commit()

        blur_mappings_to_add_to_db = []
        all_mappings_to_add_to_db = []


    

        for page_number, (blurred_page_data, all_text_page_data) in enumerate(zip(blurred_text_and_bbox, all_text_and_bbox), start=1):
            # Save post-processed page record
            new_page = PostProcessPDFPage(pdf_id=new_pdf.id, page_number=page_number, image_path=blurred_page_data["image_path"])
            session.add(new_page)
            session.flush()  # Get new_page.id

            # Save blur mappings for the page
            for mapping in blurred_page_data["blurred_text_and_bbox"]:
                blur_mapping = BlurMapping(
                    postprocessed_page_id=new_page.id,
                    bounding_box=json.dumps(mapping["coordinates"]),  # Store the bounding box as a JSON string
                    original_word=mapping["word"],
                )
                blur_mappings_to_add_to_db.append(blur_mapping)

            # Save all text mappings for the page
            for mapping in all_text_page_data["all_text_and_bbox"]:
                all_mapping = AllMapping(
                    postprocessed_page_id=new_page.id,
                    bounding_box=json.dumps(mapping["coordinates"]),
                    original_word=mapping["word"],
                )
                all_mappings_to_add_to_db.append(all_mapping)

            # Add all mappings at once to the session
            session.add_all(blur_mappings_to_add_to_db)
            session.add_all(all_mappings_to_add_to_db)

            # Commit the changes
            session.commit()
        

        

        return {"pages": "1", "blur_mappings": len(blur_mappings_to_add_to_db), "all_mappings": len(all_mappings_to_add_to_db)}

    except Exception as e:
        logger.error(f"Error during PDF processing: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing PDF.")

    finally:
        clean_up(temp_pdf_path)