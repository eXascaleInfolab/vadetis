import pandas as pd
from pandas.tseries.frequencies import to_offset
from sklearn.metrics import fbeta_score, precision_score, recall_score, accuracy_score, confusion_matrix
from vadetisweb.parameters import GEO, HISTOGRAM, CLUSTER_GAUSSIAN_MIXTURE, SVM, ISOLATION_FOREST, \
    DTW_DISTANCE_FUNCTION, GEO_DISTANCE, TIME_RANGE, ANOMALY_DETECTION_SCORE_TYPES, WINDOW_SIZE_ABSOLUTE, \
    WINDOW_SIZE_PERCENT, SELECTION, DTW, PEARSON, LISA

from .date_utils import unix_time_millis_to_dt
from .helper_function_utils import *

def is_valid_conf(conf):
    if 'algorithm' in conf:

        if conf['algorithm'] == LISA:

            if conf['correlation_algorithm'] == PEARSON:

                if isNone(conf['window_size_value']):
                    return False
                elif isNone(conf['window_size_unit']):
                    return False

                else:
                    if not isPositiveInteger(conf['window_size_value']):
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

                if isNone(conf['window_size_value']):
                    return False
                elif isNone(conf['window_size_unit']):
                    return False

                else:
                    if not isPositiveInteger(conf['window_size_value']):
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

    return True


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


def next_dt(dt, type, inferred_freq, size=1):
    """
    Provides a later or earlier datetime from the given datetime that corresponds
    to a certain frequency and size.

    :param dt: a datetime object
    :param type: either 'later' or 'earlier'
    :param freq: the frequency for the timedelta
    :param size: the size of the window (that is applied with the frequency)
    :return: the next later or earlier datetime
    """
    #print("Inferred_freq:", inferred_freq)

    if type == 'later':
        f = lambda x, y: _add(x,y)
    elif type == 'earlier':
        f = lambda  x, y: _subtract(x,y)
    else:
        raise ValueError('Wrong type provided')

    # some freqs require relative offset, others can be computed with timedelta
    if inferred_freq.endswith(('MS', 'AS', 'B', 'W', 'M', 'SM', 'BM', 'CBM', 'SMS', 'BMS', 'CBMS', 'Q', 'BQ', 'QS', 'BQS', 'A', 'Y', 'BA', 'BY', 'YS', 'BAS', 'BYS', 'BH')):
        next_dt = (f(dt, to_offset(inferred_freq) * size)).to_pydatetime()
    else:
        next_dt = f(dt, pd.to_timedelta(to_offset(inferred_freq)) * size)

    return next_dt


def zscore_for_column(column, index, skipna=True):
    """
    Returns the Z Scores of a pandas dataframe column. Mean and std will handle NaN values by default

    :param column: the column
    :param index: the index
    :return: Z-Score for column
    """

    # ddof = 0: population standard deviation using n; ddof = 1: sample std deviation using n-1
    return (column - column.mean(skipna=skipna)) / column.std(skipna=skipna, level=None, ddof=0)


def df_zscore(df, skipna=True):
    """
    Returns new pandas dataframe of Z-Score values

    :param df: the input dataframe
    :return: a dataframe of Z-Score values
    """

    df_zscore = df.apply(lambda column: zscore_for_column(column, column.name, skipna), axis=0)
    return df_zscore


def get_window_size(window_size_value, window_size_unit, df=None):

    if window_size_unit == WINDOW_SIZE_PERCENT and df is not None:
        return get_window_size_for_percentage(df, window_size_value)
    elif window_size_unit == WINDOW_SIZE_ABSOLUTE:
        return int(window_size_value)
    return 0


def get_window_size_for_percentage(df, percentage):
    return int(round((float(len(df.index)) / float(100)) * int(percentage)))


def get_dataframes_for_ranges(df, df_class, conf):

    range_start = unix_time_millis_to_dt(conf['range_start']) if conf['time_range'] == SELECTION else None
    range_end = unix_time_millis_to_dt(conf['range_end']) if conf['time_range'] == SELECTION else None

    # get only needed area of dataframe
    if range_start is not None and range_end is not None and conf['algorithm'] != LISA:
        df = df.loc[range_start:range_end]
        df_class = df_class[range_start:range_end]

    elif conf['algorithm'] == LISA:
        if conf['correlation_algorithm'] == PEARSON or conf['correlation_algorithm'] == DTW:
            window_size = get_window_size(conf['window_size_value'], conf['window_size_unit'], df)

            if range_start is not None and range_end is not None:
                # todo instead of date, may locate by number of index steps?
                range_start_offset = next_dt(range_start, 'earlier', df.index.inferred_freq, window_size - 1)

                df = df.loc[range_start_offset:range_end]
                df_class = df_class[range_start_offset:range_end]

        else:  # correlation is geo distance

            if range_start is not None and range_end is not None:
                df = df.loc[range_start:range_end]
                df_class = df_class[range_start:range_end]

    return df, df_class


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

    print('Threshold: %.3f' % threshold)
    print('Accuracy Score: %.3f' % accuracy)
    print('Recall Score: %.3f' % recall)
    print('Precision Score: %.3f' % precision)
    print('F1 Score: %.3f' % f1_score)

    return info
