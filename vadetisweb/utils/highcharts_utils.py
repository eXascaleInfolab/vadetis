import logging


def get_highcharts_range_button_preselector(inferred_freq):

    if inferred_freq is None:
        logging.warning("Warning: no granularity provided, will return default")
        return 3

    if inferred_freq.endswith(('B', 'C', 'D')): # freq of days
        return 4 # month
    elif inferred_freq.endswith(('M', 'BM', 'CBM', 'MS', 'BMS', 'CBMS')): # freq of months
        return 6 # all
    elif inferred_freq.endswith(('W', 'SM', 'SMS')): # freq of weeks or two week
        return 5 # year
    elif inferred_freq.endswith(('Q', 'BQ', 'QS', 'BQS')): # freq of quarters
        return 6 # all
    elif inferred_freq.endswith(('A', 'Y', 'BA', 'BY', 'AS', 'YS', 'BAS', 'BYS')): # freq of years
        return 6 # all
    elif inferred_freq.endswith(('BH', 'H')): # freq of hours
        return 3 # week
    elif inferred_freq.endswith(('T', 'min')):  # freq of minutes
        return 2 # day
    elif inferred_freq.endswith(('S')):  # freq of seconds
        return 0 # minute

    return 3
