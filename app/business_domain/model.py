from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database import db_session, Base

# Business Domain Model
class BusinessDomain(Base):
    __tablename__ = 'business_domain'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    general_comment = Column(String(5000), nullable=True)
    example_of_use = Column(String(5000), nullable=True)

    # Foreign key
    business_area_id = Column(Integer, ForeignKey('business_area.id'), nullable=True)
    business_area = relationship('BusinessArea', backref=backref('business_area', lazy='dynamic'))

    def __init__(self, name, general_comment, example_of_use, business_area):
        self.name = name
        self.general_comment = general_comment
        self.example_of_use = example_of_use
        self.business_area = business_area

    # Return object data in easily serializeable format
    @property
    def serialize(self):
        payload = {
            'id': self.id,
            'name': self.name,
            'general_comment': self.general_comment,
            'example_of_use': self.example_of_use,
        }
        if self.business_area is None:
            payload['business_area'] = None
        else:
            payload['business_area'] = self.business_area.serialize
        return payload
