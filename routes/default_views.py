from models.Subject import Subject
from models.Teacher import Teacher
from models.Student import Student
from models.Event import Event
from common.BaseView import BaseView
from security.decorators import is_authorized


class TeacherView(BaseView):
    __model_class__ = Teacher
    __always_expand__ = ('subjects',)


class SubjectView(BaseView):
    __model_class__ = Subject


class EventsView(BaseView):
    __model_class__ = Event


class StudentsView(BaseView):
    __model_class__ = Student

default_decorators = [is_authorized]
default_views = [TeacherView(decorators=default_decorators, base_url='/api/teachers/').get_view(),
                 SubjectView(decorators=default_decorators, base_url='/api/subjects/').get_view(),
                 EventsView(decorators=default_decorators, base_url='/api/events/').get_view(),
                 StudentsView(decorators=default_decorators, base_url='/api/students/').get_view()]
