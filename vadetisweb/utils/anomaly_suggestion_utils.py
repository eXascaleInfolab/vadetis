from vadetisweb.parameters import *
from vadetisweb.utils.date_utils import dt_to_unix_time_millis

def get_default_configuration(algorithm, dataset):
    if algorithm == LISA_PEARSON:
        return _lisa_pearson_default(dataset)
    elif algorithm == LISA_DTW_PEARSON:
        return _lisa_dtw_default(dataset)
    elif algorithm == LISA_GEO:
        return _lisa_geo_default(dataset)
    elif algorithm == RPCA_HUBER_LOSS:
        return _rpca_default(dataset)
    elif algorithm == HISTOGRAM:
        return _histogram_default(dataset)
    elif algorithm == CLUSTER_GAUSSIAN_MIXTURE:
        return _cluster_default(dataset)
    elif algorithm == SVM:
        return _svm_default(dataset)
    elif algorithm == ISOLATION_FOREST:
        return _isolation_forest_default(dataset)


def get_time_series_lisa_suggestion(dataset):
    """
    For suggestion we choose the time series with the most anomalies

    :param dataset: the dataset for suggestion
    :return: the time series we use for anomaly detection
    """
    time_series = None
    max_anomalies = 0
    for ts in dataset.timeseries_set.all():
        num_anomalies = dataset.number_of_time_series_anomaly_values(ts.id)
        if num_anomalies > max_anomalies:
            max_anomalies = num_anomalies
            time_series = ts

    return time_series


def get_time_range(dataset, offset, max_range=500):
    """
    For suggestion we do not compute over the whole dataset, as we have several algorithms and each dataset could contain up to 100'000 points
    the computation would take too long. Therefore we compute for a max index range of 500 values

    :param dataset: the dataset to determine the range for
    :param offset: an offset, e.g. for the window size for LISA
    :param max_range: the maximum index size
    :return: range_start and range_end
    """
    df = dataset.dataframe
    index_length = len(dataset.dataframe.index)
    if index_length <= max_range + offset:
        if offset == 0:
            return dt_to_unix_time_millis(df.index[0]), dt_to_unix_time_millis(df.index[-1])
        else:
            return dt_to_unix_time_millis(df.index[offset-1]), dt_to_unix_time_millis(df.index[-1])
    else:
        start_index = max_range + offset
        return dt_to_unix_time_millis(df.index[-start_index]), dt_to_unix_time_millis(df.index[-1])


def get_training_dataset(dataset):
    """
    By default we use the training dataset that has the highest contamination level (number of outliers relative to number of values)
    :param dataset: the dataset we search a training dataset for
    :return: the training dataset to use for suggestion

    """
    max_contamination_level = 0
    selected_training_dataset = None
    for training_dataset in dataset.training_dataset.all():
        contamination = training_dataset.number_of_anomaly_values() / training_dataset.number_of_normal_values()
        if contamination > max_contamination_level:
            max_contamination_level = contamination
            selected_training_dataset = training_dataset

    return selected_training_dataset


def _lisa_pearson_default(dataset):
    time_series = get_time_series_lisa_suggestion(dataset)
    range_start, range_end = get_time_range(dataset, offset=10)

    return {
        'dataset': dataset,
        'time_series': time_series.id,
        'window_size': 10,
        'normalize': True,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': F1_SCORE,
        'range_start': range_start,
        'range_end': range_end
    }


def _lisa_dtw_default(dataset):
    time_series = get_time_series_lisa_suggestion(dataset)
    range_start, range_end = get_time_range(dataset, offset=10)

    return {
        'dataset': dataset,
        'time_series': time_series.id,
        'window_size': 10,
        'dtw_distance_function': EUCLIDEAN,
        'normalize': True,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': F1_SCORE,
        'range_start': range_start,
        'range_end': range_end
    }


def _lisa_geo_default(dataset):
    time_series = get_time_series_lisa_suggestion(dataset)
    range_start, range_end = get_time_range(dataset, offset=10)

    return {
        'dataset': dataset,
        'time_series': time_series.id,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': F1_SCORE,
        'range_start': range_start,
        'range_end': range_end
    }


def _rpca_default(dataset):
    training_dataset = get_training_dataset(dataset)
    range_start, range_end = get_time_range(dataset, offset=10)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'delta': 1.0,
        'n_components': 2,
        'train_size': 0.5,
        'random_seed': 10,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': F1_SCORE,
        'range_start': range_start,
        'range_end': range_end
    }


def _histogram_default(dataset):
    training_dataset = get_training_dataset(dataset)
    range_start, range_end = get_time_range(dataset, offset=10)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'train_size': 0.5,
        'random_seed': 10,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': F1_SCORE,
        'range_start': range_start,
        'range_end': range_end
    }


def _cluster_default(dataset):
    training_dataset = get_training_dataset(dataset)
    range_start, range_end = get_time_range(dataset, offset=10)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'n_components': 3,
        'n_init': 3,
        'train_size': 0.5,
        'random_seed': 10,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': F1_SCORE,
        'range_start': range_start,
        'range_end': range_end
    }


def _svm_default(dataset):
    training_dataset = get_training_dataset(dataset)
    range_start, range_end = get_time_range(dataset, offset=10)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'kernel': KERNEL_RBF,
        'gamma': 0.0005,
        'nu' : 0.95,
        'train_size': 0.5,
        'random_seed': 10,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': F1_SCORE,
        'range_start': range_start,
        'range_end': range_end
    }


def _isolation_forest_default(dataset):
    training_dataset = get_training_dataset(dataset)
    range_start, range_end = get_time_range(dataset, offset=10)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'bootstrap': False,
        'n_estimators' : 40,
        'train_size': 0.5,
        'random_seed': 10,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': F1_SCORE,
        'range_start': range_start,
        'range_end': range_end
    }
