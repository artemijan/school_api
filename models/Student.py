from User import User
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates
from common.validators import v_not_null, v_range


class Student(User):
    __plural__ = "students"
    stage = Column(Integer, unique=False)
    stage_prefix = Column(String(2), unique=False)

    @validates('stage')
    def validate_stage(self, key, stage):
        v_not_null(key, stage)
        v_range(key, stage, min=0, max=11)
        return stage

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }
