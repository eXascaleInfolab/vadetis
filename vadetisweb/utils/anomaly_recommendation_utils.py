from vadetisweb.models import *
from vadetisweb.utils.date_utils import dt_to_unix_time_millis, unix_time_millis_to_dt
from vadetisweb.anomaly_algorithms.detection.helper_functions import df_anomaly_instances

def get_recommendation(scores):

    entries = scores['scores']
    max_nmi = max([x['nmi'] for x in entries])
    min_rmse = min([x['rmse'] for x in entries])
    max_f1_score = max([x['f1_score'] for x in entries])
    max_accuracy = max([x['accuracy'] for x in entries])
    max_precision = max([x['precision'] for x in entries])
    max_recall = max([x['recall'] for x in entries])

    best_nmi_scores = [item for item in entries if item['nmi'] == max_nmi]
    best_rmse_scores = [item for item in entries if item['rmse'] == min_rmse]
    best_f1_scores = [item for item in entries if item['f1_score'] == max_f1_score]
    best_accuracies = [item for item in entries if item['accuracy'] == max_accuracy]
    best_precisions = [item for item in entries if item['precision'] == max_precision]
    best_recalls = [item for item in entries if item['recall'] == max_recall]

    return {
        'nmi_scores': best_nmi_scores,
        'rmse_scores': best_rmse_scores,
        'f1_scores': best_f1_scores,
        'accuracies': best_accuracies,
        'precisions': best_precisions,
        'recalls': best_recalls,
    }


def get_transformed_conf(conf):
    if 'time_series' in conf:
        conf['time_series'] = TimeSeries.objects.get(id=conf['time_series']).name

    if 'training_dataset' in conf:
        conf['training_dataset'] = DataSet.objects.get(id=conf['training_dataset']).title

    if 'range_start' in conf:
        conf['range_start'] = unix_time_millis_to_dt(conf['range_start'])

    if 'range_end' in conf:
        conf['range_end'] = unix_time_millis_to_dt(conf['range_end'])

    return conf


def get_default_configuration(algorithm, maximize_score, dataset):
    if algorithm == LISA_PEARSON:
        return _lisa_pearson_default(maximize_score, dataset)
    elif algorithm == LISA_DTW_PEARSON:
        return _lisa_dtw_default(maximize_score, dataset)
    elif algorithm == LISA_SPATIAL:
        return _lisa_geo_default(maximize_score, dataset)
    elif algorithm == RPCA_HUBER_LOSS:
        return _rpca_default(maximize_score, dataset)
    elif algorithm == HISTOGRAM:
        return _histogram_default(maximize_score, dataset)
    elif algorithm == CLUSTER_GAUSSIAN_MIXTURE:
        return _cluster_default(maximize_score, dataset)
    elif algorithm == SVM:
        return _svm_default(maximize_score, dataset)
    elif algorithm == ISOLATION_FOREST:
        return _isolation_forest_default(maximize_score, dataset)


def get_time_series_recommendation(dataset):
    """
    For recommendation we choose the time series with the most anomalies

    :param dataset: the dataset for recommendation
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


def get_time_range(df, df_class, ts_id=None, max_range=500):
    """
    For recommendation we do not compute over the whole dataset, as we have several algorithms and each dataset could contain up to 100'000 points
    the computation would take too long. Therefore we compute for a max index range of "max_range" values

    :param df: the dataframe to determine the range
    :param df_class: the class dataframe to determine the most suitable range
    :param ts_id: time series id for lisa
    :param max_range: the maximum index size
    :return: range_start and range_end
    """
    index_length = len(df.index)
    if index_length <= max_range: # index length shorter than max_range => take all
        start_index = 0
        return dt_to_unix_time_millis(df.index[start_index]), dt_to_unix_time_millis(df.index[index_length-1])
    else: # get most suitable range
        start_index, end_index = _get_indexes(df_class, ts_id, max_range)
        return dt_to_unix_time_millis(df.index[start_index]), dt_to_unix_time_millis(df.index[end_index])


def _get_indexes(df_class, ts_id, max_range):
    df_common_class = df_anomaly_instances(df_class) if ts_id is None else df_class.rename(columns={ ts_id : 'class'})

    a = df_common_class['class'].values  # df as array of values
    m = np.concatenate(([False], a == True, [False]))  # mask
    anomalous_intervals = np.flatnonzero(m[1:] != m[:-1]).reshape(-1, 2)  # start-stop limits
    anomalous_start_indexes = anomalous_intervals[:, 0]
    anomalous_end_indexes = anomalous_intervals[:, 1]

    max_length = len(a) - 1
    start, end = _get_best_range(anomalous_start_indexes, anomalous_end_indexes, max_length, max_range)

    if end >= max_range:
        return end - max_range + 1, end
    else:
        return 0, max_range - 1


def _get_best_range(anomalous_start_indexes, anomalous_end_indexes, max_length, max_range):
    start = 0
    end = max_length
    max_iterate_range = 0
    for end_index in anomalous_end_indexes:
        for start_index in anomalous_start_indexes:
            if start_index <= end_index:
                range = end_index - start_index
                if range >= max_range:
                    return start, end
                elif range >= max_iterate_range:
                    start = start_index
                    end = end_index
                    max_iterate_range = range

    return start, end


def get_training_dataset(dataset):
    """
    By default we use the training dataset that has the highest contamination level (number of outliers relative to number of values)
    :param dataset: the dataset we search a training dataset for
    :return: the training dataset to use for recommendation

    """
    max_contamination_level = 0
    selected_training_dataset = None
    for training_dataset in dataset.training_dataset.all():
        contamination = training_dataset.contamination_level()
        if contamination > max_contamination_level:
            max_contamination_level = contamination
            selected_training_dataset = training_dataset

    return selected_training_dataset


def _lisa_pearson_default(maximize_score, dataset):
    time_series = get_time_series_recommendation(dataset)
    df = dataset.dataframe.copy()
    df_class = dataset.dataframe_class.copy()
    range_start, range_end = get_time_range(df, df_class, ts_id=time_series.id)

    return {
        'dataset': dataset,
        'time_series': time_series.id,
        'window_size': 10,
        'normalize': True,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': maximize_score,
        'range_start': range_start,
        'range_end': range_end
    }


def _lisa_dtw_default(maximize_score, dataset):
    time_series = get_time_series_recommendation(dataset)
    df = dataset.dataframe.copy()
    df_class = dataset.dataframe_class.copy()
    range_start, range_end = get_time_range(df, df_class, ts_id=time_series.id)

    return {
        'dataset': dataset,
        'time_series': time_series.id,
        'window_size': 10,
        'dtw_distance_function': EUCLIDEAN,
        'normalize': True,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': maximize_score,
        'range_start': range_start,
        'range_end': range_end
    }


def _lisa_geo_default(maximize_score, dataset):
    time_series = get_time_series_recommendation(dataset)
    df = dataset.dataframe.copy()
    df_class = dataset.dataframe_class.copy()
    range_start, range_end = get_time_range(df, df_class, ts_id=time_series.id)

    return {
        'dataset': dataset,
        'time_series': time_series.id,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': maximize_score,
        'range_start': range_start,
        'range_end': range_end
    }


def _rpca_default(maximize_score, dataset):
    training_dataset = get_training_dataset(dataset)
    df = dataset.dataframe.copy()
    df_class = dataset.dataframe_class.copy()
    range_start, range_end = get_time_range(df, df_class)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'delta': 1.0,
        'n_components': 2,
        'train_size': 0.5,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': maximize_score,
        'range_start': range_start,
        'range_end': range_end
    }


def _histogram_default(maximize_score, dataset):
    training_dataset = get_training_dataset(dataset)
    df = dataset.dataframe.copy()
    df_class = dataset.dataframe_class.copy()
    range_start, range_end = get_time_range(df, df_class)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'train_size': 0.5,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': maximize_score,
        'range_start': range_start,
        'range_end': range_end
    }


def _cluster_default(maximize_score, dataset):
    training_dataset = get_training_dataset(dataset)
    df = dataset.dataframe.copy()
    df_class = dataset.dataframe_class.copy()
    range_start, range_end = get_time_range(df, df_class)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'n_components': 3,
        'n_init': 3,
        'train_size': 0.5,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': maximize_score,
        'range_start': range_start,
        'range_end': range_end
    }


def _svm_default(maximize_score, dataset):
    training_dataset = get_training_dataset(dataset)
    df = dataset.dataframe.copy()
    df_class = dataset.dataframe_class.copy()
    range_start, range_end = get_time_range(df, df_class)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'kernel': KERNEL_RBF,
        'gamma': 0.0005,
        'nu': 0.95,
        'train_size': 0.5,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': maximize_score,
        'range_start': range_start,
        'range_end': range_end
    }


def _isolation_forest_default(maximize_score, dataset):
    training_dataset = get_training_dataset(dataset)
    df = dataset.dataframe.copy()
    df_class = dataset.dataframe_class.copy()
    range_start, range_end = get_time_range(df, df_class)

    return {
        'dataset': dataset,
        'training_dataset': training_dataset.id,
        'bootstrap': False,
        'n_estimators': 40,
        'train_size': 0.5,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': maximize_score,
        'range_start': range_start,
        'range_end': range_end
    }
