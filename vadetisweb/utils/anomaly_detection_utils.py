from vadetisweb.parameters import LISA, PEARSON, DTW, GEO, HISTOGRAM, CLUSTER_GAUSSIAN_MIXTURE, SVM, ISOLATION_FOREST, \
    WINDOW_SIZE_ABSOLUTE, DTW_DISTANCE_FUNCTION, WINDOW_SIZE_PERCENT, GEO_DISTANCE, TIME_RANGE, \
    ANOMALY_DETECTION_SCORE_TYPES
from .helper_function_utils import *


def is_valid_conf(conf):
    if 'algorithm' in conf:

        if conf['algorithm'] == LISA:

            if conf['correlation_algorithm'] == PEARSON:

                if isNone(conf['window_size']):
                    return False
                else:
                    window_size_list = decompress_window_size(conf['window_size'])
                    if not len(window_size_list) == 2:
                        return False

                    if not isPositiveInteger(window_size_list[0]):
                        return False

                    if not window_size_list[1] in [WINDOW_SIZE_ABSOLUTE, WINDOW_SIZE_PERCENT]:
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
                else:
                    window_size_list = decompress_window_size(conf['window_size'])
                    if not len(window_size_list) == 2:
                        return False

                    if not isPositiveInteger(window_size_list[0]):
                        return False

                    if not window_size_list[1] in [WINDOW_SIZE_ABSOLUTE, WINDOW_SIZE_PERCENT]:
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

            if not isPositiveInteger(conf['td_selected']):
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

            if not isPositiveInteger(conf['td_selected']):
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

            if not isPositiveInteger(conf['td_selected']):
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

            if not isPositiveInteger(conf['td_selected']):
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


def decompress_window_size(value, int_conversion=True):
    if value and int_conversion:
        return [int(i) if i.isdigit() else i for i in value.split('_')]
    elif value and not int_conversion:
        return [i for i in value.split('_')]
    return None
