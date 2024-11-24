from sqlalchemy import Column, Integer, String, DateTime, Float

from app.db import Base, engine


class CargoInsurance(Base):
    __tablename__ = 'cargo_insurance'
    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String(255))
    rate = Column(Float)
    date = Column(DateTime)


def create_models():
    Base.metadata.create_all(bind=engine)
