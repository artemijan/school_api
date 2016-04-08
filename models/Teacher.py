from User import User
from sqlalchemy.orm import relationship


class Teacher(User):
    __plural__ = "teachers"
    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }
    # is needed for serializable, property wouldn't be in serialized data because it's write only
    subjects = relationship("Subject", secondary='subject_teachers', back_populates="teachers")
