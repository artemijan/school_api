from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from common.db import Base
from common.utils import Serializable
from User import User
association_table = Table('subject_teachers', Base.metadata,
                          Column('subjects_id', Integer, ForeignKey('subjects.id')),
                          Column('teachers_id', Integer, ForeignKey('users.id'))
                          )


class Subject(Base, Serializable):
    __tablename__ = 'subjects'
    __plural__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    allowed_stages = Column(String(255), unique=False, nullable=False)
    class_rooms = Column(String(255), unique=False, nullable=True)
    description = Column(String(255), unique=False, nullable=True)
    teachers = relationship("Teacher", secondary=association_table, back_populates="subjects")


class Teacher(User):
    # is needed for serializable, property wouldn't be in serialized data because it's write only
    subjects = relationship("Subject", secondary=association_table, back_populates="teachers")
