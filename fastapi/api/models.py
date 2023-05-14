import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine(f"postgresql+psycopg2://admin:admin@{os.getenv('DB_URL')}/{os.getenv('DB')}", pool_pre_ping=True)

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    pk = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    login = Column(String(), nullable=False, unique=True)
    hash_password = Column(String(), nullable=False)
    first_name = Column(String(), default='Empty')
    last_name = Column(String(), default='Empty')
    other_name = Column(String(), default='Empty')
    email = Column(String(), default='Empty')
    phone = Column(String(), default='Empty')
    birthday = Column(DateTime(), default=datetime.now())
    city = Column(Integer(), ForeignKey('city.id', onupdate='CASCADE'))
    additional_info = Column(String(), default="Empty")
    is_admin = Column(Boolean(), default=False)

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer(), primary_key=True, nullable=False, unique=True)
    name = Column(Integer(), nullable=False, unique=True)


Base.metadata.create_all(bind=engine)