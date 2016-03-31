from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.orm.collections import InstrumentedList


class Serializable(object):
    __exclude__ = ('id',)
    __include__ = ()
    __serializable_props__ = ()
    __write_only__ = ()

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
                if (not (prop in exclude) | (prop in include)) & isinstance(
                        getattr(cls, prop, None), QueryableAttribute):
                    setattr(self, prop, value)
        return self

    def deserialize(self, json):
        if not json:
            return None
        return self.__class__.from_json(json, selfObj=self)

    def initialize(self):
        if len(getattr(self.__class__, '__write_only__', ())) == 0:
            self.__class__.__write_only__ = ()

        if len(getattr(self.__class__, '__serializable_props__', ())) == 0:
            self.__class__.__serializable_props__ = ()
            for key in dir(self.__class__):
                if (not key.startswith('_')) & hasattr(self.__class__, key) & isinstance(
                        getattr(self.__class__, key), QueryableAttribute):
                    self.__class__.__serializable_props__ += (key,)
        self.__class__._initialized = True

    def serialize(self, **kwargs):
        """
        Why do we need init _iterable here?
        Because __init__ method could be not called at all, for example:
        User.query.all() - since we don't call constructor, __init__ method wouldn't be called
        :param kwargs:
        :return:
        """
        if not getattr(self.__class__, '_initialized', None):
            self.initialize()
        dictionary = {}
        prop = 'props'
        # recursive call, "exclude" is needed to prevent circular dependency serialization
        exclude = kwargs.get('exclude', ())
        if (prop in kwargs) & (kwargs.get(prop, None) is not None):
            for prop in kwargs:
                if hasattr(self, prop):
                    dictionary[prop] = self[prop]
        else:
            # loop trough all accessible properties
            for key in self.__class__.__serializable_props__:
                # check if those properties are read only
                if not (key in self.__class__.__write_only__):
                    # check if property is an array
                    if isinstance(getattr(self, key, None), InstrumentedList):
                        # if this property is not excluded
                        if not (getattr(self, key)[0].__class__ in exclude):
                            # if dictionary doesn't have this property then init it
                            if not (key in dictionary) or not isinstance(dictionary[key], list):
                                dictionary[key] = []
                            if len(getattr(self, key)) > 0:
                                for li in getattr(self, key):
                                    dictionary[key].append(li.serialize(exclude=(exclude + (self.__class__,))))
                    # if not array
                    else:
                        dictionary[key] = getattr(self, key, None)
        return dictionary
