from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/fastapi_pizza"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
