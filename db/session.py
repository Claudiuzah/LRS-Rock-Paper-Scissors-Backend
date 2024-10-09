from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_PASSWORD = "0000"
DB_NAME = "RPSDB"

DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
