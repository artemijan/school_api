from flask import jsonify as jsfy
from sqlalchemy.orm.attributes import QueryableAttribute


class Serializable:

    def __init__(self):
        self.__serializable_props__ = ()

    def serialize(self, **kwargs):
        """
        Why do we need init _iterable here?
        Because __init__ method could be not called at all, for example:
        User.query.all() - since we don't call constructor, __init__ method wouldn't be called
        :param kwargs:
        :return:
        """
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
                if not (key in self.__wtite_only__):
                    dictionary[key] = getattr(self, key, None)
        return dictionary


def get_json_key(obj, key):
    if key in obj:
        return obj[key]
    else:
        return None


def merge_dictionaries(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def parse_list(listed, **kwargs):
    props = None
    accessor = None
    if 'props' in kwargs:
        props = kwargs['props']
    if 'accessor' in kwargs:
        accessor = kwargs['accessor']
    result = {}
    if isinstance(listed, (list, tuple)):
        is_array = True
        if len(listed) > 0:
            if hasattr(type(listed[0]), '__plural__') and not accessor:
                accessor = getattr(type(listed[0]), '__plural__')
            elif not accessor:
                accessor = getattr(type(listed[0]), '__tablename__')
            result[accessor] = []
        for list_item in listed:
            if isinstance(list_item, Serializable):
                if is_array:
                    result[accessor].append(list_item.serialize(props=props))
                else:
                    result[type(list_item).__name__.lower()] = list_item.serialize(props=props)
    else:
        result = None
    return result


def jsonify(*args, **kwargs):
    """
    This function converts (list, tuple) to dictionary and returns JSONify representation.
    Remember that this method put into json objects which has "serialize()" method,
    that returns dict representation of this object
    :param props:
    :param args:
    :param kwargs:
    :return: JSON
    """
    props = None
    if 'props' in kwargs:
        props = kwargs['props']
    result = {}
    for arg in args:
        if isinstance(arg, Serializable):
            result = merge_dictionaries(result, arg.serialize(props=props))
        else:
            # set accessor (just a key in dict where we store an array) for list or tuple only
            if isinstance(arg, (list, tuple)):
                result = merge_dictionaries(result, parse_list(arg, props=props))
            elif isinstance(arg, dict):
                for accessor, list_item in arg.items():
                    if isinstance(list_item, Serializable):
                        result[accessor].append(list_item.serialize(props=props))
                    elif isinstance(list_item, (list, tuple)):
                        result = merge_dictionaries(result, parse_list(list_item, accessor=accessor, props=props))
                    else:
                        result[accessor] = list_item
    for key, value in kwargs.items():
        if isinstance(value, (list, tuple)):
            result[key] = []
            for list_item in value:
                if isinstance(list_item, Serializable):
                    result[key].append(list_item.serialize(props=props))
    return jsfy(result)
