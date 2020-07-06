import logging
import pandas as pd
from pandas.tseries.frequencies import to_offset
from sklearn.metrics import fbeta_score, precision_score, recall_score, accuracy_score, confusion_matrix
from vadetisweb.parameters import *

from .date_utils import unix_time_millis_to_dt
from .helper_function_utils import *
"""
def is_valid_conf(conf):
    if 'algorithm' in conf:

        if conf['algorithm'] == LISA_PEARSON: #TODO other lisa parameters

            if conf['correlation_algorithm'] == PEARSON:

                if isNone(conf['window_size']):
                    return False
                elif isNone(conf['window_size_unit']):
                    return False

                else:
                    if not isPositiveInteger(conf['window_size']):
                        return False

                    if not conf['window_size_unit'] in [WINDOW_SIZE_ABSOLUTE, WINDOW_SIZE_PERCENT]:
                        return False

                if isinstance(conf['min_periods'], int):
                    if not isPositiveInteger(conf['min_periods']):
                        return False

                    if conf['min_periods'] > conf['window_size']:
                        return False

                elif not isNone(conf['min_periods']):
                    return False

                if not isBoolean(conf['row_standardized']):
                    return False

                if not isValidSelection(conf['time_range'], TIME_RANGE):
                    return False

                if not isValidSelection(conf['maximize_score'], ANOMALY_DETECTION_SCORE_TYPES):
                    return False

                if not isPositiveInteger(conf['range_start']):
                    return False

                if not isPositiveInteger(conf['range_end']):
                    return False

                if not conf['range_end'] > conf['range_start']:
                    return False

            elif conf['correlation_algorithm'] == DTW:

                if isNone(conf['window_size']):
                    return False
                elif isNone(conf['window_size_unit']):
                    return False

                else:
                    if not isPositiveInteger(conf['window_size']):
                        return False

                    if not conf['window_size_unit'] in [WINDOW_SIZE_ABSOLUTE, WINDOW_SIZE_PERCENT]:
                        return False

                if not isValidSelection(conf['dtw_distance_function'], DTW_DISTANCE_FUNCTION):
                    return False

                if not isBoolean(conf['row_standardized']):
                    return False

                if not isValidSelection(conf['time_range'], TIME_RANGE):
                    return False

                if not isValidSelection(conf['maximize_score'], ANOMALY_DETECTION_SCORE_TYPES):
                    return False

                if not isPositiveInteger(conf['range_start']):
                    return False

                if not isPositiveInteger(conf['range_end']):
                    return False

                if not conf['range_end'] > conf['range_start']:
                    return False

            elif conf['correlation_algorithm'] == GEO:

                if not isValidSelection(conf['geo_distance_function'], GEO_DISTANCE):
                    return False

                if not isBoolean(conf['row_standardized']):
                    return False

                if not isValidSelection(conf['time_range'], TIME_RANGE):
                    return False

                if not isValidSelection(conf['maximize_score'], ANOMALY_DETECTION_SCORE_TYPES):
                    return False

                if not isPositiveInteger(conf['range_start']):
                    return False

                if not isPositiveInteger(conf['range_end']):
                    return False

                if not conf['range_end'] > conf['range_start']:
                    return False
            else:
                return False

        elif conf['algorithm'] == HISTOGRAM:

            if not isPositiveInteger(conf['training_dataset']):
                return False

            if not isFloatInRange(0, 1, conf['train_size']):
                return False

            if not isPositiveInteger(conf['random_seed']):
                if not isNone(conf['random_seed']):
                    return False

            if not isValidSelection(conf['time_range'], TIME_RANGE):
                return False

            if not isValidSelection(conf['maximize_score'], ANOMALY_DETECTION_SCORE_TYPES):
                return False

            if not conf['range_end'] > conf['range_start']:
                return False

        elif conf['algorithm'] == CLUSTER_GAUSSIAN_MIXTURE:

            if not isPositiveInteger(conf['training_dataset']):
                return False

            if not isFloatInRange(0, 1, conf['train_size']):
                return False

            if not isPositiveInteger(conf['random_seed']):
                if not isNone(conf['random_seed']):
                    return False

            if not isPositiveInteger(conf['n_components']):
                return False

            if not isPositiveInteger(conf['n_init']):
                return False

            if not isValidSelection(conf['time_range'], TIME_RANGE):
                return False

            if not isValidSelection(conf['maximize_score'], ANOMALY_DETECTION_SCORE_TYPES):
                return False

            if not conf['range_end'] > conf['range_start']:
                return False

        elif conf['algorithm'] == SVM:

            if not isPositiveInteger(conf['training_dataset']):
                return False

            if not isFloatInRange(0, 1, conf['train_size']):
                return False

            if not isPositiveInteger(conf['random_seed']):
                if not isNone(conf['random_seed']):
                    return False

            if isinstance(conf['gamma'], str):
                if not conf['gamma'] == 'auto':
                    return False
            else:
                if not isFloatInRange(0, 1, conf['gamma']):
                    return False

            if not isFloatInNuRange(conf['nu']):
                return False

            if not isValidSelection(conf['time_range'], TIME_RANGE):
                return False

            if not isValidSelection(conf['maximize_score'], ANOMALY_DETECTION_SCORE_TYPES):
                return False

            if not conf['range_end'] > conf['range_start']:
                return False

        elif conf['algorithm'] == ISOLATION_FOREST:

            if not isPositiveInteger(conf['training_dataset']):
                return False

            if not isFloatInRange(0, 1, conf['train_size']):
                return False

            if not isPositiveInteger(conf['random_seed']):
                if not isNone(conf['random_seed']):
                    return False

            if not isBoolean(conf['bootstrap']):
                return False

            if not isPositiveInteger(conf['n_estimators']):
                return False

            if not isValidSelection(conf['time_range'], TIME_RANGE):
                return False

            if not isValidSelection(conf['maximize_score'], ANOMALY_DETECTION_SCORE_TYPES):
                return False

            if not conf['range_end'] > conf['range_start']:
                return False

        else:
            return False
    else:
        return False

    return True"""


def _add(x, y):
    """
    Adds to values
    :param x: first value
    :param y: second value
    :return: result of the addition
    """

    return x + y

def _subtract(x, y):
    """
    Subtracts two values
    :param x: first value
    :param y: second value
    :return: result of the subtraction
    """

    return x - y


def next_dt(dt, f, inferred_freq, size=1):
    """
    Provides a later or earlier datetime from the given datetime that corresponds
    to a certain frequency and size.

    :param dt: a datetime object
    :param f: a function to either subtract or add two datetime object
    :param freq: the frequency for the timedelta
    :param size: the size of the window (that is applied with the frequency)
    :return: the next later or earlier datetime
    """

    """if type == 'later':
        f = lambda x, y: _add(x,y)
    elif type == 'earlier':
        f = lambda x, y: _subtract(x,y)
    else:
        raise ValueError('Wrong type provided')"""

    # some freqs require relative offset, others can be computed with timedelta
    if inferred_freq.endswith(('MS', 'AS', 'B', 'W', 'M', 'SM', 'BM', 'CBM', 'SMS', 'BMS', 'CBMS', 'Q', 'BQ', 'QS', 'BQS', 'A', 'Y', 'BA', 'BY', 'YS', 'BAS', 'BYS', 'BH')):
        next_dt = (f(dt, to_offset(inferred_freq) * size)).to_pydatetime()
    else:
        next_dt = f(dt, pd.to_timedelta(to_offset(inferred_freq)) * size)

    return next_dt


def next_earlier_dt(dt, inferred_freq, size=1):
    return next_dt(dt, lambda x, y: _subtract(x,y), inferred_freq, size)


def next_later_dt(dt, inferred_freq, size=1):
    return next_dt(dt, lambda x, y: _add(x,y), inferred_freq, size)


def zscore_for_column(column, index, skipna=True):
    """
    Returns the Z Scores of a pandas dataframe column. Mean and std will handle NaN values by default

    :param column: the column
    :param index: the index
    :param skipna: defines if to skip NaN values
    :return: Z-Score for column
    """

    # ddof = 0: population standard deviation using n; ddof = 1: sample std deviation using n-1
    return (column - column.mean(skipna=skipna)) / column.std(skipna=skipna, level=None, ddof=0)


def df_zscore(df, skipna=True):
    """
    Transforms a dataframe to z-score values

    :param df: the dataframe of raw data
    :param skipna: defines if to skip NaN values
    :return: a dataframe of Z-Score values
    """

    df_zscore = df.apply(lambda column: zscore_for_column(column, column.name, skipna), axis=0)
    return df_zscore


"""def get_window_size(df,window_size, window_size_unit):
    if window_size_unit == WINDOW_SIZE_PERCENT:
        return get_window_size_for_percentage(df, window_size)

    elif window_size_unit == WINDOW_SIZE_ABSOLUTE:
        return int(window_size)

    else:
        raise ValueError


def get_window_size_for_percentage(df, percentage):
    return int(round((float(len(df.index)) / float(100)) * int(percentage)))"""


"""def get_dataframes_for_ranges(df, df_class, conf):

    range_start = unix_time_millis_to_dt(conf['range_start']) if conf['time_range'] == SELECTION else None
    range_end = unix_time_millis_to_dt(conf['range_end']) if conf['time_range'] == SELECTION else None

    # get only needed area of dataframe
    if range_start is not None and range_end is not None and conf['algorithm'] != LISA_PEARSON:
        df = df.loc[range_start:range_end]
        df_class = df_class[range_start:range_end]

    elif conf['algorithm'] == LISA_PEARSON:
        if conf['correlation_algorithm'] == PEARSON or conf['correlation_algorithm'] == DTW:
            window_size = conf['window_size']

            if range_start is not None and range_end is not None:
                # todo instead of date, may locate by number of index steps?
                range_start_offset = next_earlier_dt(range_start, df.index.inferred_freq, window_size - 1)

                df = df.loc[range_start_offset:range_end]
                df_class = df_class[range_start_offset:range_end]

        else:  # correlation is geo distance

            if range_start is not None and range_end is not None:
                df = df.loc[range_start:range_end]
                df_class = df_class[range_start:range_end]

    return df, df_class"""


def get_info(threshold, y_hat_results, y_truth):
    info = {}

    accuracy = accuracy_score(y_pred=y_hat_results, y_true=y_truth)
    recall = recall_score(y_pred=y_hat_results, y_true=y_truth)
    precision = precision_score(y_pred=y_hat_results, y_true=y_truth)
    f1_score = fbeta_score(y_pred=y_hat_results, y_true=y_truth, beta=1)

    cnf_matrix = confusion_matrix(y_truth, y_hat_results)
    info['cnf_matrix'] = cnf_matrix.tolist()

    info['threshold'] = threshold
    info['accuracy'] = accuracy
    info['recall'] = recall
    info['precision'] = precision
    info['f1_score'] = f1_score

    logging.debug('Threshold: %.3f' % threshold)
    logging.debug('Accuracy Score: %.3f' % accuracy)
    logging.debug('Recall Score: %.3f' % recall)
    logging.debug('Precision Score: %.3f' % precision)
    logging.debug('F1 Score: %.3f' % f1_score)

    return info
