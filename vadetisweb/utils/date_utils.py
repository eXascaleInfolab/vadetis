import datetime, pytz

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


def unix_time_millis_from_dt(dt):
    """
    Computes the unix time from a given datetime
    If the datetime dt has a different timezone as UTC it will be replaced with UTC,
    which results in a timeshifted unix UTC time in millis (shifted by the timezone offset)

    :param dt: a datetime
    :return: the unix time of the given datetime
    """
    epoch = datetime.datetime.utcfromtimestamp(0)
    epoch = epoch.replace(tzinfo=pytz.utc)
    #time = dt.astimezone(pytz.utc)
    time = dt.replace(tzinfo=pytz.utc)

    return (time - epoch).total_seconds() * 1000.0