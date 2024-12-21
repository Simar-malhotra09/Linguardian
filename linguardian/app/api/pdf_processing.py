from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from services.pdf_processing import process_pdf
# from services.return_text import return_text
from database.database import get_db

router = APIRouter()

@router.post("/process-pdf")
async def pro_pdf(file: UploadFile = File(...), session: Session = Depends(get_db)):
    return await process_pdf(file, session)

# @router.post("/return-text")
# async def pro_pdf(file: UploadFile = File(...), session: Session = Depends(get_db)):
#     return await return_text(file, session)


