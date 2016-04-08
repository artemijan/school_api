from User import User
from sqlalchemy import Column, String, Integer


class Student(User):
    __plural__ = "students"
    stage = Column(Integer, unique=False)
    stage_prefix = Column(String(2), unique=False)
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }
