from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base  

# Set up your database URL
DATABASE_URL = "sqlite:///./test_linguardian.db"  

# Create an engine that knows how to connect to your database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # connect_args for SQLite

# Create a session maker that can create sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database (this would normally be run at the application startup)
Base.metadata.create_all(bind=engine)

# Dependency to get the session in your FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
