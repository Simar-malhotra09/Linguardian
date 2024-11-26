
from fastapi import FastAPI
from api import pdf_processing

app = FastAPI()
app.include_router(pdf_processing.router)


# import os
# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import FileResponse, JSONResponse
# from linguardian.linguardian import Linguardian
# import shutil
# from uuid import uuid4
# from datetime import datetime, timezone
# import json
# import logging

# logging.basicConfig(level=logging.DEBUG)

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# from linguardian.app.models.models import Base,ProcessedPDF,PreProcessPDFPage, PostProcessPDFPage,BlurMapping
# from linguardian.lib.save_images_from_pdf import save_pdf_as_images

# app = FastAPI()

# engine= create_engine("sqlite:///linguardian.db", echo=True)
# Base.metadata.create_all(bind=engine)

# Session= sessionmaker(bind=engine)
# session=Session()



# '''create a temp local copy of the pdf,
#     apply processes and for now return the 
#     images in a zip folder.
# '''

# @app.post("/process-pdf")
# async def process_pdf(file: UploadFile = File(...)):
    
#     session = Session()  # Create a database session

#     ''' Create a temp pdf for the uploaded file '''
#     unique_filename = f"{uuid4().hex}.pdf"
#     temp_pdf_path=unique_filename


#     pre_process_images = f"/Users/simarmalhotra/Desktop/projects/romaji-redacter/images/pre_process_images/{unique_filename}/"
#     post_process_images = f"/Users/simarmalhotra/Desktop/projects/romaji-redacter/images/post_process_images/{unique_filename}/"

#     if not os.path.exists(pre_process_images):
#         os.makedirs(pre_process_images)
#     if not os.path.exists(post_process_images):
#         os.makedirs(post_process_images)



#     try:

#         #  Step 1: Save the uploaded PDF temporarily
#         with open(temp_pdf_path, "wb") as f:
#             f.write(await file.read())

#         image_paths = save_pdf_as_images(temp_pdf_path, pre_process_images)


#         # Step 2: Add PDF metadata to the database
#         new_pdf = ProcessedPDF(file_name=file.filename ,file_path=pre_process_images)
#         session.add(new_pdf)
#         session.commit()

#         # Step 3: Process the PDF
#         linguardian = Linguardian(temp_pdf_path, post_process_images)
#         output_images_data = linguardian.process_pdf()  

#         # Step 4: Process and save page and blur mapping data
#         blur_mappings_to_add = []
#         response_data=[]

#         for page_number, page_data in enumerate(output_images_data, start=1):
            
            
#             image_path = page_data["image_path"]
#             blurred_words_and_bbox = page_data["blurred_words_and_bbox"]

#             # Save the postprocessed page record
#             new_page = PostProcessPDFPage(pdf_id=new_pdf.id, page_number=page_number, image_path=image_path)
#             session.add(new_page)
#             session.flush()  

#             # Collect data for response
#             response_data.append({
#                 "page_number": page_number,
#                 "image_path": image_path,  
#                 "blurred_words": blurred_words_and_bbox
#             })
            


#             # Prepare blur mappings for the current page
#             for mapping in blurred_words_and_bbox:
#                 blur_mapping = BlurMapping(
#                     postprocessed_page_id=new_page.id,
#                     bounding_box=json.dumps(mapping["coordinates"]),
#                     original_word=mapping["word"],
#                 )
#                 blur_mappings_to_add.append(blur_mapping)

#         # Batch insert blur mappings
#         session.add_all(blur_mappings_to_add)
#         session.commit()
#         logging.info("PDF processing and data insertion completed successfully.")
        
#         return JSONResponse(content={"message": "Processing complete", "data": response_data})


#     except Exception as e:
#         print(f"Error processing PDF: {e}")
#         session.rollback()
#         return JSONResponse(content={"error": str(e)}, status_code=500)

#     finally:
#         if os.path.exists(temp_pdf_path):
#             os.remove(temp_pdf_path)

#         session.close()