from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.database import db_session, Base

# Service Domain Model
class ServiceDomain(Base):
    __tablename__ = 'service_domain'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    general_comment = Column(String(5000), nullable=True)
    example_of_use = Column(String(5000), nullable=True)

    # Foreign key
    business_domain_id = Column(Integer, ForeignKey('business_domain.id'), nullable=True)
    business_domain = relationship('BusinessDomain', backref=backref('business_domain', lazy='dynamic'))

    def __init__(self, name, general_comment, example_of_use, business_domain):
        self.name = name
        self.general_comment = general_comment
        self.example_of_use = example_of_use
        self.business_domain = business_domain

    # Return object data in easily serializeable format
    @property
    def serialize(self):
        payload = {
            'id': self.id,
            'name': self.name,
            'general_comment': self.general_comment,
            'example_of_use': self.example_of_use,
        }
        if self.business_domain is None:
            payload['business_domain'] = None
        else:
            payload['business_domain'] = self.business_domain.serialize
        return payload
