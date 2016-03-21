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
            if hasattr(list_item, 'as_dict'):
                if is_array:
                    result[accessor].append(list_item.as_dict(props=props))
                else:
                    result[type(list_item).__name__.lower()] = list_item.as_dict(props=props)
    else:
        result = None
    return result


def jsonify(*args, **kwargs):
    """
    This function converts (list, tuple) to dictionary and returns JSONify representation.
    Remember that this method put into json objects which has "as_dict()" method,
    that returns dict representation of this object
    :param props:
    :param args:
    :param kwargs:
    :return: JSON
    """
    if 'props' in kwargs:
        props = kwargs['props']
    result = {}
    for arg in args:
        if hasattr(arg, 'as_dict'):
            result = merge_dictionaries(result, arg.as_dict(props=props))
        else:
            # set accessor (just a key in dict where we store an array) for list or tuple only
            if isinstance(arg, (list, tuple)):
                result = merge_dictionaries(result, parse_list(arg, props=props))
            elif isinstance(arg, dict):
                for accessor, list_item in arg.items():
                    if hasattr(list_item, 'as_dict'):
                        result[accessor].append(list_item.as_dict(props=props))
                    elif isinstance(list_item, (list, tuple)):
                        result = merge_dictionaries(result, parse_list(list_item, accessor=accessor, props=props))
    for key, value in kwargs.items():
        if isinstance(value, (list, tuple)):
            result[key] = []
            for list_item in value:
                if hasattr(list_item, 'as_dict'):
                    result[key].append(list_item.as_dict(props=props))
    return jsfy(result)
