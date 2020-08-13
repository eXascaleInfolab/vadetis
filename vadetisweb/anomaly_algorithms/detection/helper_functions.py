import logging
import numpy as np
import pandas as pd
from sklearn.metrics import fbeta_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import train_test_split

from vadetisweb.parameters import F1_SCORE, PRECISION, RECALL, ACCURACY, NMI, RMSE
from vadetisweb.utils import unix_time_millis_to_dt, next_earlier_dt


def df_range(df, df_class, range_start_millis, range_end_millis, start_offset=None):
    range_start = unix_time_millis_to_dt(range_start_millis)
    if start_offset is not None:
        range_start = next_earlier_dt(range_start, df.index.inferred_freq, start_offset - 1)
        if range_start < df.index[0]:
            logging.warning(
                "You selected a window size of {}, but first timestamp {} is out of bounds. Fallback to minimum index.".format(start_offset, range_start))
            range_start = df.index[0]

    range_end = unix_time_millis_to_dt(range_end_millis)

    if range_start is not None and range_end is not None:
        df_range = df.loc[range_start:range_end]
        df_class_range = df_class[range_start:range_end]
    else:
        raise ValueError("Timestamps could not be converted")

    return df_range, df_class_range


def df_copy_with_mean(df, axis=1, skipna=True):
    """
    Returns a copy of the dataframe, including a column with mean values

    :param df: a dataframe
    :param axis: 1 for row-wise, 0 for columns
    :return: Copy of dataframe, with mean values
    """
    df_mean = df.copy()

    if 'mean' not in df_mean.columns:
        df_mean['mean'] = df_mean.mean(skipna=skipna, axis=axis)

    return df_mean


def df_copy_empty(df):
    """
    Returns an empty copy of a dataframe with same indexes and columns

    :param df: the data frame to copy
    :return: empty copy of the dataframe
    """
    return pd.DataFrame().reindex_like(df)


def _df_remove_column(df, column_name):
    """
    Removes a column froma dataframe
    :param df: a dataframe
    :param column_name: the column (name) to remove
    """
    if column_name in df.columns:
        del df[column_name]


def arrElemContainsTrue(x):
    """
    Helper method to check if a 1-dim arr contains 1
    :param x: a 1-dim array
    :return: 0 if it does not contain 1, 1 otherwise
    """
    return np.any(x == 1).astype(int)


def get_max_score_index_for_score_type(threshold_scores, score_type):
    if score_type == RECALL:
        return threshold_scores[:, 0].argmax()
    elif score_type == PRECISION:
        return threshold_scores[:, 1].argmax()
    elif score_type == F1_SCORE:
        return threshold_scores[:, 2].argmax()
    elif score_type == ACCURACY:
        return threshold_scores[:, 3].argmax()
    elif score_type == NMI:
        return threshold_scores[:, 4].argmax()
    elif score_type == RMSE:
        return threshold_scores[:, 5].argmin()  # best RMSE is lowest value

    raise ValueError


def df_anomaly_instances(df_class):
    df_class_instances = pd.DataFrame(index=df_class.index)
    df_class_instances['class'] = False

    indexes = []
    for index, row in df_class.iterrows():
        for column in df_class.columns:
            if row[column] == 1:
                indexes.append(index)
                break
    logging.debug('Number of anomaly instances: %d', len(indexes))

    for index in indexes:
        df_class_instances.loc[index, 'class'] = True

    return df_class_instances


def estimate_score_bound(lower, higher):
    logging.debug('Threshold Normal: %f', higher)
    logging.debug('Threshold Anomaly: %f', lower)

    higher_bound = (higher + np.abs((higher / 100) * 20))  # .astype(int)
    lower_bound = (lower - np.abs((lower / 100) * 20))  # .astype(int)

    logging.debug('Higher Bound %f', higher_bound)
    logging.debug('Lower Bound %f', lower_bound)

    return lower_bound, higher_bound


def get_train_valid_sets(df_train, train_size=0.5, random_seed=10):
    """
    Splits the training dataset into a train and validation set. Use this method for semi supervised techniques
    as those models should be trained with only normal data.

    :param df_train: training data set with normal and anomalous data, should contain a "class" column to indicate anomalies
    :param train_size: the proportion of the dataset to include in the split
    :param random_seed: the seed used by the random number generator

    :return: a train set of normal data, a validation test set of normal and anomalous data
    """
    normal = df_train[df_train['class'] == False]
    anomalous = df_train[df_train['class'] == True]

    train, normal_test, _, _ = train_test_split(normal, normal,
                                                train_size=train_size,
                                                random_state=random_seed)

    normal_valid, _, _, _ = train_test_split(normal_test, normal_test,
                                             train_size=train_size,
                                             random_state=random_seed)

    anomalous_valid, _, _, _ = train_test_split(anomalous, anomalous,
                                                train_size=train_size,
                                                random_state=random_seed)

    valid = normal_valid.append(anomalous_valid).sample(frac=1, random_state=random_seed)

    logging.debug('Train shape: %s' % repr(train.shape))
    logging.debug('Valid shape: %s' % repr(valid.shape))
    logging.debug('Proportion of anomaly in validation set: %.2f\n' % valid['class'].mean())

    return train, valid
