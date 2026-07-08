from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ecommerce_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Hàm Dependency cung cấp Database Session cho API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()