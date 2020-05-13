import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import fbeta_score, precision_score, recall_score, accuracy_score, confusion_matrix

from vadetisweb.parameters import F1_SCORE, PRECISION, RECALL, ACCURACY

def _sequences_from_path(x, y, path):
    #print("x:", x)
    #print("path_x:", path[0])
    x_dtw = x[path[0]]
    #print("y:", y)
    #print("path_y:", path[1])
    y_dtw = y[path[1]]

    return x_dtw, y_dtw


def df_row_standardized(df):
    """
    Makes a dataframe row standardized (rows sum to one), denumerator must be absolute value as
    signs should not be changed by division.

    :param df: the dataframe to apply row standardization
    :return: a row standardized dataframe
    """
    #todo division by zero, replace({ 0 : np.nan })?, example: series 2, gaussian distr ts
    #https://stackoverflow.com/questions/44241521/dataframe-element-wise-divide-by-sum-of-row-inplace
    df_std = df.div((df.abs().sum(axis=1)), axis=0)

    return df_std


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


def _sum_of_squares(values):
    """
    Squares each value of a list of values and returns the sum of it

    :param values: a list of values
    :return: the sum of squared values
    """
    return sum(n ** 2 for n in values)


def get_threshold_scores(thresholds, y_scores, valid, upper_boundary=False):
    """
    Computes for each possible threshold the score for the performance metrics
    TODO only compute the score we aim for??

    :param thresholds: a list of possible thresholds
    :param y_scores: the list of computed scores by the detection algorithm
    :param valid: the true class values to run the performance metric against
    :param upper_boundary: determines if score higher than thresholds are anomalies or not

    :return: array of scores for each threshold for each performance metric
    """
    scores = []

    # its possible that y_scores is a multidim array containing NaN
    # however, any comparison (other than !=) of a NaN to a non-NaN value will always return False,
    # and therefore will not be detected as anomaly
    with np.errstate(invalid='ignore'):

        for threshold in thresholds:
            y_hat = np.array(y_scores < threshold).astype(int) if upper_boundary == False else np.array(y_scores > threshold).astype(int)

            # check if multidim array
            if y_hat.ndim > 1:
                y_hat = np.apply_along_axis(arrElemContainsTrue, 1, y_hat)

            scores.append([recall_score(y_true=valid['class'].values, y_pred=y_hat),
                           precision_score(y_true=valid['class'].values, y_pred=y_hat),
                           fbeta_score(y_true=valid['class'].values, y_pred=y_hat, beta=1),
                           accuracy_score(y_true=valid['class'].values, y_pred=y_hat)])

    return np.array(scores)


def arrElemContainsTrue(x):
    """
    Helper method to check if a 1-dim arr contains 1
    :param x: a 1-dim array
    :return: 0 if it does not contain 1, 1 otherwise
    """
    return np.any(x == 1).astype(int)


def get_max_score_index_for_score_type(threshold_scores, score_type):
    if score_type == F1_SCORE:
        return threshold_scores[:, 2].argmax()
    elif score_type == RECALL:
        return threshold_scores[:, 0].argmax()
    elif score_type == PRECISION:
        return threshold_scores[:, 1].argmax()
    elif score_type == ACCURACY:
        return threshold_scores[:, 3].argmax()
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
    print('Number of anomaly instances:', len(indexes))

    for index in indexes:
        df_class_instances.loc[index, 'class'] = True

    return df_class_instances


def estimate_score_bound(lower, higher):
    print('Threshold Normal', higher)
    print('Threshold Anomaly', lower)

    #TODO higher-lower ???
    higher_bound = (higher + np.abs((higher / 100) * 20)) #.astype(int)
    lower_bound = (lower - np.abs((lower / 100) * 20)) #.astype(int)

    print('Higher Bound', higher_bound)
    print('Lower Bound', lower_bound)

    return lower_bound, higher_bound


def get_train_valid_test_sets(df_train, train_size=0.5, random_seed=10):
    """
    Splits the training dataset into a train, validation and test set. Use this method for semi supervised techniques
    as those models should be trained with only normal data.

    :param df_train: training data set with normal and anomalous data, should contain a class column to indicate anomalies
    :param train_size: the proportion of the dataset to include in the train split
    :param random_seed: the seed used by the random number generator

    :return: a train set of normal data, a valid test set of normal and anomalous data, a test set of normal and anomalous data
    """
    normal = df_train[df_train['class'] == False]
    anomaly = df_train[df_train['class'] == True]

    train, normal_test, _, _ = train_test_split(normal, normal,
                                                train_size=train_size,
                                                random_state=random_seed)

    normal_valid, normal_test, _, _ = train_test_split(normal_test, normal_test,
                                                       train_size=train_size,
                                                       random_state=random_seed)

    anormal_valid, anormal_test, _, _ = train_test_split(anomaly, anomaly,
                                                         train_size=train_size,
                                                         random_state=random_seed)

    #train = train  # .reset_index(drop=True)
    valid = normal_valid.append(anormal_valid).sample(frac=1, random_state=random_seed)
    test = normal_test.append(anormal_test).sample(frac=1, random_state=random_seed)

    print('Train shape: ', train.shape)
    print('Proportion of anomaly in training set: %.2f\n' % train['class'].mean())
    print('Valid shape: ', valid.shape)
    print('Proportion of anomaly in validation set: %.2f\n' % valid['class'].mean())
    print('Test shape:, ', test.shape)
    print('Proportion of anomaly in test set: %.2f\n' % test['class'].mean())

    return train, valid, test
