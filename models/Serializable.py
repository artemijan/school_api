from sqlalchemy.orm.attributes import QueryableAttribute


class Serializable(object):
    __exclude__ = ('id',)
    __include__ = ()
    __serializable_props__ = ()
    __write_only__ = ()

    @classmethod
    def from_json(cls, json):
        self = cls()
        exclude = (cls.__exclude__ or ()) + Serializable.__exclude__
        include = cls.__include__ or ()
        if json:
            for prop, value in json.iteritems():
                # ignore all non user data, e.g. only
                if (not (prop in exclude) | (prop in include)) & isinstance(
                        getattr(cls, prop, None), QueryableAttribute):
                    setattr(self, prop, value)
        return self

    def serialize(self, **kwargs):
        """
        Why do we need init _iterable here?
        Because __init__ method could be not called at all, for example:
        User.query.all() - since we don't call constructor, __init__ method wouldn't be called
        :param kwargs:
        :return:
        """

        if len(getattr(self, '__write_only__', ())) == 0:
            self.__write_only__ = ()

        if len(getattr(self, '__iterable__', ())) == 0:
            self.__serializable_props__ = ()
            for key in dir(self.__class__):
                if (not key.startswith('_')) & hasattr(self.__class__, key) & isinstance(
                        getattr(self.__class__, key), QueryableAttribute):
                    self.__serializable_props__ += (key,)
        dictionary = {}
        prop = 'props'
        if (prop in kwargs) & (kwargs[prop] is not None):
            for prop in kwargs:
                if hasattr(self, prop):
                    dictionary[prop] = self[prop]
        else:
            for key in self.__serializable_props__:
                if not (key in self.__write_only__):
                    dictionary[key] = getattr(self, key, None)
        return dictionary