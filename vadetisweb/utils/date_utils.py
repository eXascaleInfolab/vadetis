import datetime

def format_time(x):
    """
    Returns a string representation of a datetime object

    :param x: a datetime object
    :return: string representation of datetime
    """
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    if isinstance(x, datetime.timedelta):
        return x.__str__()
    raise TypeError("Unknown type")