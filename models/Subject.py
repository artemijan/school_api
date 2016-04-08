from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from common.db import Base
from common.utils import Serializable
from Teacher import Teacher
association_table = Table('subject_teachers', Base.metadata,
                          Column('subjects_id', Integer, ForeignKey('subjects.id')),
                          Column('teachers_id', Integer, ForeignKey('users.id'))
                          )


class Subject(Base, Serializable):
    __tablename__ = 'subjects'
    __plural__ = 'subjects'
    __mapper_args__ = {
        'polymorphic_identity': 'subject'
    }
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    allowed_stages = Column(String(255), unique=False, nullable=False)
    class_rooms = Column(String(255), unique=False, nullable=True)
    description = Column(String(255), unique=False, nullable=True)
    teachers = relationship(Teacher, secondary='subject_teachers', back_populates="subjects")
