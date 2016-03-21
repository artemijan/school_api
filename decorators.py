from sqlalchemy.orm.attributes import QueryableAttribute


def as_dict(*args):
    _dict = {}
    if args:
        for prop in args[0].__props__:
            _dict[prop] = getattr(args[0], prop)
    return _dict


def get_public_props(cls):
    public_props = (name for name in vars(cls) if not name.startswith('_'))
    return public_props


def dict_model(*args, **kwargs):
    def wrapper(cls):
        cls.__props__ = {}
        iterable = dir(cls)
        if len(kwargs.items()) > 0:
            iterable = kwargs
        for name in iterable:
            if (not name.startswith('_')) & isinstance(getattr(cls, name), QueryableAttribute):
                cls.__props__[name] = None
        cls.as_dict = as_dict
        return cls

    if (len(kwargs.items()) > 0) or not args:
        return wrapper
    else:
        return wrapper(args[0])
