from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Use DATABASE_URL from settings. Example for Postgres:
# postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Engine creation: only pass sqlite-specific args when using sqlite
engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


