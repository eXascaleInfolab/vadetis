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


def unix_time_millis_to_dt_str(unix_millis):
    """
    Converts a given unix time into a string representation

    :param unix_millis: the unix time
    :return: a string representation of the unix time
    """
    value_sec = float(unix_millis) / 1000
    dt = datetime.datetime.fromtimestamp(value_sec).strftime('%Y-%m-%d %H:%M:%S')
    return dt


def unix_time_millis_to_dt(unix_millis):
    """
    Converts a unix time to a datetime object

    :param unix_millis: the unix time
    :return: a datetime object
    """

    value_sec = float(unix_millis) / 1000
    dt = datetime.datetime.fromtimestamp(value_sec)
    return dt
