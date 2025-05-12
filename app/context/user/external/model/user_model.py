from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import CITEXT
from app.main.config.database.db import Base

class UserModel(Base):
    __tablename__ = 'app_users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    document = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    salt = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
    
    class Config:
        orm_mode = True