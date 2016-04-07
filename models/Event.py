from sqlalchemy import Column, Integer, String, DateTime
from common.db import Base
from common.utils import Serializable
from datetime import datetime


class Event(Base, Serializable):
    __tablename__ = 'events'
    __plural__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False, nullable=False)
    date = Column(DateTime(timezone=False), unique=False, nullable=False)
    description = Column(String(255), unique=False, nullable=True)
    location = Column(String(255), unique=False, nullable=True)

    def __init__(self):
        if self.date is None:
            self.date = datetime.now()
