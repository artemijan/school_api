from flask import jsonify as jsfy


def merge_dictionaries(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def jsonify(*args, **kwargs):
    """
    This function converts (list, tuple) to dictionary and returns JSONify representation.
    Remember that this method put into json objects which has "as_dict()" method,
    that returns dict representation of this object
    :param args:
    :param kwargs:
    :return: JSON
    """
    result = {}
    for arg in args:
        if hasattr(arg, 'as_dict'):
            result = merge_dictionaries(result, arg.as_dict())
        else:
            is_array = False
            # set accessor (just a key in dict where we store an array) for list or tuple only
            if isinstance(arg, (list, tuple)):
                is_array = True
                if len(arg) > 0:
                    if hasattr(type(arg[0]), '__plural__'):
                        accessor = getattr(type(arg[0]), '__plural__')
                    else:
                        accessor = getattr(type(arg[0]), '__tablename__')
                    result[accessor] = []
            else:
                accessor = type(arg).__name__.lower()
            for list_item in arg:
                if hasattr(list_item, 'as_dict'):
                    if is_array:
                        result[accessor].append(list_item.as_dict())
                    else:
                        result[type(list_item).__name__.lower()] = list_item.as_dict()
    for key, value in kwargs.items():
        if isinstance(value, (list, tuple)):
            result[key] = []
            for list_item in value:
                if hasattr(list_item, 'as_dict'):
                    result[key].append(list_item.as_dict())
    return jsfy(result)
