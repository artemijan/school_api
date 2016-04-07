from models.Subject import Teacher, Subject
from common.BaseView import BaseView


class TeacherView(BaseView):
    __model_class__ = Teacher


class SubjectView(BaseView):
    __model_class__ = Subject


default_views = [TeacherView(decorators=[], base_url='/api/teachers/').get_blueprint(),
                 SubjectView(decorators=[], base_url='/api/subjects/').get_blueprint()]
