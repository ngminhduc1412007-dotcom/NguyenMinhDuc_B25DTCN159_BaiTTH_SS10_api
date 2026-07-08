from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_URL = "mysql+pymysql://root:123456@localhost:3306/student_db"

engine = create_engine(DB_URL)
Base.metadata.create_all(bind=engine)

LocalSession = sessionmaker(
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()