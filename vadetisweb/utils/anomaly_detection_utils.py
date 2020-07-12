import pandas as pd, logging
from pandas.tseries.frequencies import to_offset
from sklearn.metrics import fbeta_score, precision_score, recall_score, accuracy_score, confusion_matrix
from vadetisweb.parameters import *

from .helper_function_utils import *


def get_detection_choices(dataset, with_empty=True):
    empty_choice = ('', '----')
    has_training_data = dataset.number_of_training_datasets() > 0
    if dataset is not None:
        if dataset.is_spatial() and has_training_data:
            if with_empty:
                return (empty_choice,) + ANOMALY_DETECTION_ALGORITHMS
            else:
                return ANOMALY_DETECTION_ALGORITHMS

        elif dataset.is_spatial() and not has_training_data:
            if with_empty:
                return (empty_choice,) + ANOMALY_DETECTION_ALGORITHMS_NON_TRAINING
            else:
                return ANOMALY_DETECTION_ALGORITHMS_NON_TRAINING

        elif not dataset.is_spatial() and has_training_data:
            if with_empty:
                return (empty_choice,) + ANOMALY_DETECTION_ALGORITHMS_NON_SPATIAL
            else:
                return ANOMALY_DETECTION_ALGORITHMS_NON_SPATIAL

        else:
            if with_empty:
                return (empty_choice,) + ANOMALY_DETECTION_ALGORITHMS_NON_SPATIAL_NON_TRAINING
            else:
                return ANOMALY_DETECTION_ALGORITHMS_NON_SPATIAL_NON_TRAINING
    else:
        if with_empty:
            return empty_choice
        else:
            raise ValueError('Could not determine supported outlier algorithms.')


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


def get_detection_meta(threshold, y_hat_results, y_truth, upper_boundary=False):
    info = {}

    accuracy = accuracy_score(y_pred=y_hat_results, y_true=y_truth)
    recall = recall_score(y_pred=y_hat_results, y_true=y_truth, zero_division=0)
    precision = precision_score(y_pred=y_hat_results, y_true=y_truth, zero_division=0)
    f1_score = fbeta_score(y_pred=y_hat_results, y_true=y_truth, beta=1, zero_division=0)

    # we set labels 0,1 manually because the dataset could contain only one class
    cnf_matrix = confusion_matrix(y_truth, y_hat_results, labels=[0,1])
    info['cnf_matrix'] = cnf_matrix.tolist()

    info['threshold'] = threshold
    info['accuracy'] = accuracy
    info['recall'] = recall
    info['precision'] = precision
    info['f1_score'] = f1_score

    info['upper_boundary'] = upper_boundary

    logging.debug('Threshold: %.3f' % threshold)
    logging.debug('Accuracy Score: %.3f' % accuracy)
    logging.debug('Recall Score: %.3f' % recall)
    logging.debug('Precision Score: %.3f' % precision)
    logging.debug('F1 Score: %.3f' % f1_score)

    return info
