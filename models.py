from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

Base = declarative_base()

class Ziplies(Base):
    __tablename__ = "Ziplies"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(200), nullable=False)
    zipcode = Column(String(10), index=True, nullable=False)
    name = Column(String(100), nullable=False)  # Creator's name
    #score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    device_id = Column(String(64), nullable=False)
