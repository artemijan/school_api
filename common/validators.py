def v_range(*args, **kwargs):
    value = args[1]
    key = args[0]
    min_value = kwargs.get('min', value)
    max_value = kwargs.get('max', value)
    if not (min_value <= value <= max_value):
        raise ValueError("Range value error of {0} : should be in range [{1},{2}]".format(key, min_value, max_value))
    return value


def v_not_null(*args, **kwargs):
    value = args[1]
    key = args[0]
    if value is None:
        raise ValueError("Not null value error for key: {0}".format(key))
    return value


def v_positive(*args, **kwargs):
    value = args[1]
    key = args[0]
    if value <= 0:
        raise ValueError("Positive value error for key: {0}".format(key))
    return value


def v_negative(*args, **kwargs):
    value = args[1]
    key = args[0]
    if value >= 0:
        raise ValueError("Negative value error for key: {0}".format(key))
    return value


def v_max_length(*args, **kwargs):
    value = args[1]
    key = args[0]
    max_length = kwargs.get('max_length', -1)
    if isinstance(value, str) and max_length > -1:
        if len(value) > max_length:
            raise ValueError("Max length value error for key: {0}".format(key))
    else:
        raise ValueError("{0} value should be a string.".format(key))
    return value


def v_min_length(*args, **kwargs):
    value = args[1]
    key = args[0]
    min_length = kwargs.get('max_length', -1)
    if isinstance(value, str) and min_length > -1:
        if len(value) < min_length:
            raise ValueError("Min length value error for key: {0}".format(key))
    else:
        raise ValueError("{0} value should be a string.".format(key))
    return value
