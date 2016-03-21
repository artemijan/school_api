from sqlalchemy import Column, Integer, String
from db import Base
from decorators import *


@dict_model(name=None, email=None)
class User(Base):
    __tablename__ = 'users'
    __plural__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %>' % self.name

    def as_dict(self):
        return {"name": getattr(self, 'name'), "email": getattr(self, 'email')}
