from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Date

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(150), default= False, nullable= False)
    username = Column(String(150), default= False, nullable= False)
    password = Column(String(150), default= False, nullable= False)
    date_created = Column(Date)
