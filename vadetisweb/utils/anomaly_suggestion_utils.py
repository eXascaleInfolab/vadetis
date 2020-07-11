from vadetisweb.parameters import *


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


def _lisa_pearson_default(dataset):
    return {
        'dataset': dataset,
        'time_series': None,
        'window_size': 10,
        'normalize': True,
        'time_range': TIME_RANGE_SELECTION,
        'maximize_score': F1_SCORE,
        'range_start': 0,
        'range_end': 0
    }


def _lisa_dtw_default(dataset):
    pass


def _lisa_geo_default(dataset):
    pass


def _rpca_default(dataset):
    pass


def _histogram_default(dataset):
    pass


def _cluster_default(dataset):
    pass


def _svm_default(dataset):
    pass


def _isolation_forest_default(dataset):
    pass
