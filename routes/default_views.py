from models.Subject import Teacher, Subject
from models.Event import Event
from common.BaseView import BaseView
from security.decorators import is_authorized


class TeacherView(BaseView):
    __model_class__ = Teacher


class SubjectView(BaseView):
    __model_class__ = Subject


class EventsView(BaseView):
    __model_class__ = Event


default_decorators = [is_authorized]
default_views = [TeacherView(decorators=default_decorators, base_url='/api/teachers/').get_view(),
                 SubjectView(decorators=default_decorators, base_url='/api/subjects/').get_view(),
                 EventsView(decorators=default_decorators, base_url='/api/events/')]
