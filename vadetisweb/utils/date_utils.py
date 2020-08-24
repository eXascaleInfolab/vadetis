import datetime
import pytz


def iso_format_time(dt):
    """
    Returns a iso string representation of a datetime object

    :param dt: a datetime object
    :return: string representation of datetime
    """
    if isinstance(dt, datetime.datetime):
        return dt.isoformat()
    if isinstance(dt, datetime.timedelta):
        return dt.__str__()
    raise TypeError("Unknown type")


def epoch_to_iso8601(unix_millis, timespec=None):
    """
    epoch_to_iso8601 - convert the unix epoch time into a iso8601 formatted date
    """
    value_sec = float(unix_millis) / 1000
    return datetime.datetime.fromtimestamp(value_sec).astimezone(pytz.utc).replace(tzinfo=None).isoformat() if timespec is None else datetime.datetime.fromtimestamp(value_sec).astimezone(pytz.utc).replace(tzinfo=None).isoformat(timespec=timespec)


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


def unix_time_millis_to_dt_str(unix_millis, dense=False):
    """
    Converts a given unix time into a string representation

    :param unix_millis: the unix time
    :return: a string representation of the unix time
    """
    value_sec = float(unix_millis) / 1000
    if not dense:
        return datetime.datetime.fromtimestamp(value_sec).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.fromtimestamp(value_sec).strftime('%Y%m%d%H%M%S')


def unix_time_millis_to_dt(unix_millis):
    """
    Converts a unix time to a datetime object

    :param unix_millis: the unix time
    :return: a datetime object
    """

    value_sec = float(unix_millis) / 1000
    #dt = datetime.datetime.fromtimestamp(value_sec)
    dt = datetime.datetime.utcfromtimestamp(value_sec)
    return dt


def dt_to_unix_time_millis(dt):
    """
    Converts a datetime into unix time with millisecond precision
    :param dt: the datetime to convert
    :return: unix time with millisecond percision
    """
    return dt.timestamp() * 1e3