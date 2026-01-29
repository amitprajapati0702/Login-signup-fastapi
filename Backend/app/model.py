import datetime
from app.Database import Base
from sqlalchemy import Column, DateTime,Integer,String


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True , index=True)
    username = Column(String , nullable=False)
    email = Column(String, nullable=False,unique=True)
    password = Column(String,nullable=False)
    role = Column(String,nullable=False,default="user")
    created_at = Column(DateTime,nullable=False,default=datetime.datetime.utcnow)
    # Adding OTP Fields
    otp = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    is_verified = Column(Integer, nullable=False, default=0)

