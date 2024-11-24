import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declared_attr

from app.config import settings


engine = sqlalchemy.create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CustomBase(object):
    @declared_attr
    def __tablename__(cls):
        """Generate table name automatically"""
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)
