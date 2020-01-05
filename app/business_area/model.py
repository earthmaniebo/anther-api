from sqlalchemy import Column, Integer, String
from app.database import db_session, Base

# Business Area Model
class BusinessArea(Base):
    __tablename__ = 'business_area'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(5000), nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    # Return object data in easily serializeable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
