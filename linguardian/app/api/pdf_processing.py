from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from services.pdf_processing import process_pdf
from database.database import get_db

router = APIRouter()

@router.post("/process-pdf")
async def pro_pdf(file: UploadFile = File(...), session: Session = Depends(get_db)):
    return await process_pdf(file, session)


    # try:
    #     # Pass the db session into the Linguardian class constructor
    #     linguardian = Linguardian(file=file, post_process_images="data/images/post_process_images", 
    #                               db=db)
        
    #     # Process the PDF with Linguardian
    #     result = linguardian.process_pdf()

    #     return {"message": "Processing complete", "data": result}

    # except Exception as e:
    #     db.rollback()  # Rollback if any exception occurs
    #     raise HTTPException(status_code=500, detail=str(e))

    # finally:
    #     db.close()  # Always close the session


# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
# from sqlalchemy.orm import Session
# from app.linguardian import Linguardian
# from app.database.database import get_db, SessionLocal  # Import the session management function

# router = APIRouter()

# @router.post("/process-pdf")
# async def process_images(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     try:
#         # Initialize Linguardian with the uploaded file and desired output path for processed images
#         linguardian = Linguardian(file=file, post_process_images="path_to_save_images")
        
#         # Process the PDF with Linguardian
#         result = linguardian.process_pdf()

#         # Optionally, you can use `db` to save details to the database if needed
#         # Example: Save PDF data into the ProcessedPDF table
#         # pdf_entry = ProcessedPDF(file_name=file.filename, file_length=len(file.file), file_path="path_to_file")
#         # db.add(pdf_entry)
#         # db.commit()

#         return {"message": "Processing complete", "data": result}

#     except Exception as e:
#         db.rollback()  # Rollback if any exception occurs
#         raise HTTPException(status_code=500, detail=str(e))

#     finally:
#         db.close()  # Always close the session
