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
        raise ValueError("Not null value error of {0}".format(key))
    return value
