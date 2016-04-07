from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.orm import RelationshipProperty
from common.db import session
from sqlalchemy.orm import class_mapper
import sqlalchemy


class Serializable(object):
    __exclude__ = ('id',)
    __include__ = ()
    __write_only__ = ()

    @classmethod
    def _attribute_names(cls):
        return [prop.key for prop in class_mapper(cls).iterate_properties if
                isinstance(prop, sqlalchemy.orm.ColumnProperty)]

    def _handle_list_of_relations(self, prop, ids):
        related_ids = map(lambda item: item.id, getattr(self, prop))
        if set(ids) == set(related_ids):
            return None
        target_class = getattr(self.__class__, prop).property.mapper.class_
        if len(ids) > 0:
            instances = session.query(target_class).filter(target_class.id.in_(ids)).all()
            setattr(self, prop, instances)
        else:
            setattr(self, prop, [])

    def _handle_single_relation(self, prop, id_):
        if getattr(self, prop).id == id_:
            return None
        target_class = getattr(self.__class__, prop).property.mapper.class_
        inst = session.query(target_class).get(id_)
        setattr(self, prop, inst)

    @classmethod
    def from_json(cls, json, selfObj=None):
        if selfObj is None:
            self = cls()
        else:
            self = selfObj
        exclude = (cls.__exclude__ or ()) + Serializable.__exclude__
        include = cls.__include__ or ()
        if json:
            for prop, value in json.iteritems():
                # ignore all non user data, e.g. only
                if (not (prop in exclude) or (prop in include)) and isinstance(getattr(cls, prop, None),
                                                                               QueryableAttribute):
                    if isinstance(getattr(self, prop), list):
                        self._handle_list_of_relations(prop, value)
                    elif isinstance(getattr(self, prop), RelationshipProperty):
                        self._handle_single_relation(prop, value)
                    else:
                        setattr(self, prop, value)
        self.__cache_dict__ = self.__dict__.copy()
        return self

    def deserialize(self, json):
        if not json:
            return None
        return self.__class__.from_json(json, selfObj=self)

    @classmethod
    def serialize_list(cls, object_list=[]):
        output = []
        for li in object_list:
            if isinstance(li, Serializable):
                serialized = li.serialize()
                if serialized:
                    output.append(li.serialize())
            else:
                output.append(li)
        return output

    def serialize(self, **kwargs):

        # init write only props
        if len(getattr(self.__class__, '__write_only__', ())) == 0:
            self.__class__.__write_only__ = ()
        dictionary = {}
        expand = kwargs.get('expand', ()) or ()
        prop = 'props'
        if expand:
            setattr(self, '__cache_dict__', None)
            # expand all the fields
            for key in expand:
                getattr(self, key)
        cache = getattr(self, '__cache_dict__', None)
        if cache is None or cache.get('id', None) is None:
            iterable = self.__dict__
        else:
            iterable = cache
        is_custom_property_set = False
        # include only properties passed as parameter
        if (prop in kwargs) and (kwargs.get(prop, None) is not None):
            is_custom_property_set = True
            iterable = kwargs.get(prop, None)
        # loop trough all accessible properties
        for key in iterable.items():
            accessor = key
            if isinstance(key, tuple):
                accessor = key[0]
            if not (accessor in self.__class__.__write_only__) and not accessor.startswith('_'):
                # force select from db to be able get relationships
                if is_custom_property_set:
                    getattr(self, accessor, None)
                if isinstance(iterable.get(accessor), list):
                    dictionary[accessor] = self.__class__.serialize_list(object_list=iterable.get(accessor))
                # check if those properties are read only
                elif isinstance(iterable.get(accessor), Serializable):
                    dictionary[accessor] = iterable.get(accessor).serialize()
                else:
                    dictionary[accessor] = iterable.get(accessor)
        return dictionary
