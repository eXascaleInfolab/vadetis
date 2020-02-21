import numpy as np

from vadetisweb.models import TimeSeries
from vadetisweb.parameters import LISA

from .anomaly_detection_utils import df_zscore
from .date_utils import unix_time_millis_from_dt
from .anomaly_detection_utils import get_info

def get_dataset_with_marker_json(dataset, type, show_anomaly, settings):
    data_series = []
    time_series = dataset.timeseries_set.all()

    # get dataframe of the series
    if type == 'zscore':
        df = df_zscore(dataset.dataframe)  # z-score values
    else:
        df = dataset.dataframe  # raw data

    for ts in time_series:
        measurements = []
        for index, value in df.loc[:, ts.id].iteritems():
            if not show_anomaly:
                measurements.append({'x': unix_time_millis_from_dt(index), 'y': value})
            else:
                df_class = dataset.dataframe_class
                outlier_color = settings['color_outliers']

                if df_class.loc[index, ts.id] == False:
                    measurements.append({'x': unix_time_millis_from_dt(index), 'y': value})
                else:
                    measurements.append({'x': unix_time_millis_from_dt(index), 'y': value,
                                         'marker': {'fillColor': outlier_color, 'radius': 3}})

        dict_series = {'id': ts.id,
                       'name': ts.name,
                       'unit': ts.unit,
                       'is_spatial': ts.is_spatial,
                       'type': type,
                       'measurements': measurements
                       }
        data_series.append(dict_series)

    return data_series


def get_predicted_dataset_with_marker_json(id, df_with_class_instances, scores, y_hat_results, settings):

    measurements = []
    for index, value in df_with_class_instances.loc[:, id].iteritems():

        integer_index = df_with_class_instances.index.get_loc(index)
        predicted_result = y_hat_results[integer_index]
        score = scores[integer_index]

        anomaly_class = 1 if (df_with_class_instances.loc[index, 'Class'] == True) else 0

        if df_with_class_instances.loc[index, 'Class'] == True and predicted_result == True: #true positive
            measurements.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': anomaly_class, 'marker': {'fillColor': settings['color_true_positive'], 'radius': 3}})

        elif df_with_class_instances.loc[index, 'Class'] == True and predicted_result == False: #false negative
            measurements.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': anomaly_class, 'marker': {'fillColor': settings['color_false_negative'], 'radius': 3}})

        elif df_with_class_instances.loc[index, 'Class'] == False and predicted_result == True: #false positive
            measurements.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': anomaly_class, 'marker': {'fillColor': settings['color_false_positive'], 'radius': 3}})

        elif df_with_class_instances.loc[index, 'Class'] == False and predicted_result == False: #true negative
            measurements.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': anomaly_class, 'marker': {'enabled': False } })

    return measurements


def get_data_series_measurements(id, df_with_class_instances, y_hat_results):

    measurements = []
    for index, value in df_with_class_instances.loc[:, id].iteritems():
        measurements.append({'x': unix_time_millis_from_dt(index), 'y': value, 'marker': {'radius': 0}})

    return measurements


def get_anomaly_detection_single_ts_results_json(dataset, ts_id, df_with_class_instances, y_hat_results, settings):
    data = {}
    data_series = []

    df_z = df_zscore(df_with_class_instances.drop('Class', axis=1))
    df_z_with_class_instances = df_z.join(df_with_class_instances['Class'])

    corr_time_series = dataset.timeseries_set.all().exclude(id=ts_id)
    ts = TimeSeries.objects.get(id=ts_id)

    # ts
    raw_measurements = get_predicted_dataset_with_marker_json(ts.id, df_with_class_instances, y_hat_results, settings)
    z_measurements = get_predicted_dataset_with_marker_json(ts.id, df_z_with_class_instances, y_hat_results, settings)

    dict_series = {'id': ts.id, 'name': ts.name, 'unit': ts.unit, 'is_spatial': ts.is_spatial,
                   'measurements': {'raw': raw_measurements, 'zscore': z_measurements}}
    data_series.append(dict_series)

    #correlated ts
    for corr_ts in corr_time_series:
        raw_measurements = get_data_series_measurements(corr_ts.id, df_with_class_instances.drop('Class', axis=1), y_hat_results)
        z_measurements = get_data_series_measurements(corr_ts.id, df_z, y_hat_results)

        dict_series = {'id': corr_ts.id, 'name': corr_ts.name, 'unit': corr_ts.unit, 'is_spatial': corr_ts.is_spatial,
                       'measurements': {'raw': raw_measurements, 'zscore': z_measurements}}
        data_series.append(dict_series)

    data['series'] = data_series

    return data


def get_anomaly_detection_ts_results_json(dataset, df_with_class_instances, scores, y_hat_results, settings):
    data = {}
    data_series = []
    time_series = dataset.timeseries_set.all()

    #todo remove
    #df_z = df_zscore(df_with_class_instances.drop('Class', axis=1))
    #df_z_with_class_instances = df_z.join(df_with_class_instances['Class'])

    for ts in time_series:
        raw_measurements = get_predicted_dataset_with_marker_json(ts.id, df_with_class_instances, scores, y_hat_results, settings)
        #z_measurements = get_predicted_dataset_with_marker_json(ts.id, df_z_with_class_instances, scores, y_hat_results, settings)

        dict_series = {'id' : ts.id,
                       'name' : ts.name,
                       'unit' : ts.unit,
                       'is_spatial' : ts.is_spatial,
                       'type' : 'raw',
                       'measurements' : raw_measurements
                       }

        data_series.append(dict_series)

    return data_series


def _set_marker_for_threshold(measurement, threshold, settings):
    if measurement['class'] == 1 and measurement['score'] < threshold: #true positive
        measurement['marker'] = {'fillColor': settings['color_true_positive'], 'radius': 3}
    elif measurement['class'] == 1 and measurement['score'] >= threshold: #false negative
        measurement['marker'] = {'fillColor': settings['color_false_negative'], 'radius': 3}
    elif measurement['class'] == 0 and measurement['score'] < threshold:  #false positive
        measurement['marker'] = {'fillColor': settings['color_false_positive'], 'radius': 3}
    elif measurement['class'] == 0 and measurement['score'] >= threshold:  # true negative
        measurement['marker'] = {'enabled': False }
        """
        if 'marker' in measurement:
            del measurement['marker']"""


def _get_scores_and_truth_from_series_measurements(series_measurements):
    scores = []
    truth = []
    for measurement in series_measurements:
        scores.append(measurement['score'])
        truth.append(measurement['class'])

    return np.array(scores), np.array(truth)


def get_updated_dataset_series_for_threshold_with_marker_json(threshold, dataset_series, info, algorithm, settings):

    for series in dataset_series:
        for measurement in series['measurements']:
            _set_marker_for_threshold(measurement, threshold, settings)

    if algorithm != LISA: #todo if not lisa we detected anomalous instance not point, so points at the same timestamp have the same truth and score
        series_first = dataset_series[0]
        series_first_measurements = series_first['measurements']
        scores, truth = _get_scores_and_truth_from_series_measurements(series_first_measurements)
        y_hat_results = (scores < threshold).astype(int)
        new_info = get_info(threshold, y_hat_results, truth)
        new_info['thresholds'] = info['thresholds']
        new_info['threshold_scores'] = info['threshold_scores']
    else:
        #todo
        info = {}

    return dataset_series, new_info
