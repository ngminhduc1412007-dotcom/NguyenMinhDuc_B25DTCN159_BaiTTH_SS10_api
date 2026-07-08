from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class ShipmentModel(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True)
    tracking_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), default="PREPARING")