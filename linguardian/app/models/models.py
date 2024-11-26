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

    # Relationships to preprocessed and postprocessed pages
    preprocessed_pages = relationship("PreProcessPDFPage", back_populates="pdf", cascade="all, delete-orphan")
    postprocessed_pages = relationship("PostProcessPDFPage", back_populates="pdf", cascade="all, delete-orphan")

# Table for preprocessed pages of a PDF
class PreProcessPDFPage(Base):
    __tablename__ = 'preprocessed_pdf_pages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pdf_id = Column(Integer, ForeignKey("processed_pdfs.id"))
    page_number = Column(Integer, nullable=False)
    image_path = Column(Text)

    # Relationship to parent PDF
    pdf = relationship("ProcessedPDF", back_populates="preprocessed_pages")

    # Relationship to blur mappings
    blur_mappings = relationship("BlurMapping", back_populates="preprocessed_page", cascade="all, delete-orphan")

# Table for postprocessed pages of a PDF
class PostProcessPDFPage(Base):
    __tablename__ = 'postprocessed_pdf_pages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pdf_id = Column(Integer, ForeignKey("processed_pdfs.id"))
    page_number = Column(Integer, nullable=False)
    image_path = Column(Text)

    # Relationship to parent PDF
    pdf = relationship("ProcessedPDF", back_populates="postprocessed_pages")

    # Relationship to blur mappings
    blur_mappings = relationship("BlurMapping", back_populates="postprocessed_page", cascade="all, delete-orphan")

# Table for blur-to-word mappings
class BlurMapping(Base):
    __tablename__ = 'blur_mappings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    preprocessed_page_id = Column(Integer, ForeignKey("preprocessed_pdf_pages.id"), nullable=True)
    postprocessed_page_id = Column(Integer, ForeignKey("postprocessed_pdf_pages.id"), nullable=True)
    bounding_box = Column(JSON, nullable=False)  # x, y, width, height
    original_word = Column(String, nullable=False)

    # Relationships to parent pages
    preprocessed_page = relationship("PreProcessPDFPage", back_populates="blur_mappings")
    postprocessed_page = relationship("PostProcessPDFPage", back_populates="blur_mappings")
