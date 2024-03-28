from sqlalchemy import Column, Integer, String
from .base import Base


# Database table representation, for SQLAlchemy and repository layer only
class User(Base):
    name = Column(String)
    email = Column(String, primary_key=True)
    password_hash = Column(String)
