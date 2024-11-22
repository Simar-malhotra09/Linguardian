from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Table for uploaded PDFs
class ProcessedPDF(Base):
    __tablename__ = 'processed_pdfs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    file_length = Column(Integer, nullable=False, default=0)  
    file_path = Column(String, nullable=True)

    # Relationship to pages
    pages = relationship("PDFPage", back_populates="pdf")

# Table for pages of a PDF
class PDFPage(Base):
    __tablename__ = 'pdf_pages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pdf_id = Column(Integer, ForeignKey("processed_pdfs.id"))
    page_number = Column(Integer, nullable=False)
    image_path = Column(Text)

    # Relationship to parent PDF
    pdf = relationship("ProcessedPDF", back_populates="pages")

    # Relationship to blur mappings
    blur_mappings = relationship("BlurMapping", back_populates="page")

# Table for blur-to-word mappings
class BlurMapping(Base):
    __tablename__ = 'blur_mappings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer, ForeignKey("pdf_pages.id"))
    bounding_box = Column(JSON, nullable=False)  # x, y, width, height
    original_word = Column(String, nullable=False)

    # Relationship to parent page
    page = relationship("PDFPage", back_populates="blur_mappings")


