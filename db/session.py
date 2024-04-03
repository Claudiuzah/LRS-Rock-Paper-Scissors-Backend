from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_PASSWORD = "0000"
DB_NAME = "RPSDB"
# engine = create_engine(f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/{DB_NAME}")
#

DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class, which is a factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
