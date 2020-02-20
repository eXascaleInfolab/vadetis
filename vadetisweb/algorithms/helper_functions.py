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


def get_threshold_scores(thresholds, y_scores, valid):
    scores = []

    for threshold in thresholds:
        y_hat = (y_scores < threshold).astype(int)
        scores.append([recall_score(y_pred=y_hat, y_true=valid['Class'].values),
                       precision_score(y_pred=y_hat, y_true=valid['Class'].values),
                       fbeta_score(y_pred=y_hat, y_true=valid['Class'].values, beta=1),
                       accuracy_score(y_pred=y_hat, y_true=valid['Class'].values)])

    return np.array(scores)


def get_info(selected_threshold, y_hat_results, y_truth):
    info = {}

    accuracy = accuracy_score(y_pred=y_hat_results, y_true=y_truth)
    recall = recall_score(y_pred=y_hat_results, y_true=y_truth)
    precision = precision_score(y_pred=y_hat_results, y_true=y_truth)
    f1_score = fbeta_score(y_pred=y_hat_results, y_true=y_truth, beta=1)

    cnf_matrix = confusion_matrix(y_truth, y_hat_results)
    info['cnf_matrix'] = cnf_matrix.tolist()

    info['selected_threshold'] = selected_threshold
    info['accuracy'] = accuracy
    info['recall'] = recall
    info['precision'] = precision
    info['f1_score'] = f1_score

    print('Selected threshold: %.3f' % selected_threshold)
    print('Accuracy Score: %.3f' % accuracy)
    print('Recall Score: %.3f' % recall)
    print('Precision Score: %.3f' % precision)
    print('F1 Score: %.3f' % f1_score)

    return info


def get_max_score_index_for_score_type(threshold_scores, score_type):
    if score_type == F1_SCORE:
        return threshold_scores[:, 2].argmax()
    elif score_type == RECALL:
        return threshold_scores[:, 0].argmax()
    elif score_type == PRECISION:
        return threshold_scores[:, 1].argmax()
    elif score_type == ACCURACY:
        return threshold_scores[:, 3].argmax()
    return None


def df_anomaly_instances(df_class):
    df_class_instances = pd.DataFrame(index=df_class.index)
    df_class_instances['Class'] = False

    indexes = []
    for index, row in df_class.iterrows():
        for column in df_class.columns:
            if row[column] == 1:
                indexes.append(index)
                break
    print('Number of anomaly instances:', len(indexes))

    for index in indexes:
        df_class_instances.loc[index, 'Class'] = True

    return df_class_instances


def estimate_score_bound(lower, higher):
    print('Threshold Normal', higher)
    print('Threshold Anomaly', lower)

    higher_bound = (higher + np.abs((higher / 100) * 20)) #.astype(int)
    lower_bound = (lower - np.abs((lower / 100) * 20)) #.astype(int)

    print('Higher Bound', higher_bound)
    print('Lower Bound', lower_bound)

    return lower_bound, higher_bound


def get_train_valid_test_sets(df_train, train_size=0.5, random_seed=42):

    normal = df_train[df_train['Class'] == False]
    anomaly = df_train[df_train['Class'] == True]

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
    print('Proportion of anomaly in training set: %.2f\n' % train['Class'].mean())
    print('Valid shape: ', valid.shape)
    print('Proportion of anomaly in validation set: %.2f\n' % valid['Class'].mean())
    print('Test shape:, ', test.shape)
    print('Proportion of anomaly in test set: %.2f\n' % test['Class'].mean())

    return train, valid, test
