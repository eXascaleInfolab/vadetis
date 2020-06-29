import numpy as np, pandas as pd

from vadetisweb.models import TimeSeries
from vadetisweb.parameters import LISA_PEARSON

from .anomaly_detection_utils import df_zscore
from .date_utils import unix_time_millis_from_dt
from .anomaly_detection_utils import get_info


def dataset_to_json(dataset, df, df_class, show_anomaly, settings, type):
    data_series = []
    time_series = dataset.timeseries_set.all()

    outlier_color = settings['color_outliers']

    for ts in time_series:
        data = []
        for index, value in df.loc[:, ts.id].iteritems():
            anomaly_class = 1 if (df_class.loc[index, ts.id] == True) else 0

            if not show_anomaly:
                if anomaly_class == 0:
                    data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'class': anomaly_class})
                else:
                    data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'class': anomaly_class})
            else:
                if anomaly_class == 0:
                    data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'class': anomaly_class})
                else:
                    data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'class': anomaly_class, 'marker': {'fillColor': outlier_color, 'radius': 3}})

        dict_series = {
            'id': ts.id,
            'name': ts.name,
            'unit': ts.unit,
            'is_spatial': ts.is_spatial(),
            'type': type,
            'data': data
        }
        data_series.append(dict_series)

    return data_series


def get_predicted_series_data_json(series_id, df_with_class_instances, scores, y_hat_results, settings):

    data = []
    for index, value in df_with_class_instances.loc[:, series_id].iteritems():

        integer_index = df_with_class_instances.index.get_loc(index)
        predicted_result = y_hat_results[integer_index]
        score = scores[integer_index]

        anomaly_class = 1 if (df_with_class_instances.loc[index, 'class'] == True) else 0

        if df_with_class_instances.loc[index, 'class'] == True and predicted_result == True: # true positive
            data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': anomaly_class, 'marker': {'fillColor': settings['color_true_positive'], 'radius': 3}})

        elif df_with_class_instances.loc[index, 'class'] == True and predicted_result == False: # false negative
            data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': anomaly_class, 'marker': {'fillColor': settings['color_false_negative'], 'radius': 3}})

        elif df_with_class_instances.loc[index, 'class'] == False and predicted_result == True: # false positive
            data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': anomaly_class, 'marker': {'fillColor': settings['color_false_positive'], 'radius': 3}})

        elif df_with_class_instances.loc[index, 'class'] == False and predicted_result == False: # true negative
            data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': anomaly_class, 'marker': {'enabled': False }})

    return data


def get_data_series_measurements(id, df_with_class_instances, y_hat_results):

    measurements = []
    for index, value in df_with_class_instances.loc[:, id].iteritems():
        measurements.append({'x': unix_time_millis_from_dt(index), 'y': value, 'marker': {'radius': 0}})

    return measurements


def get_anomaly_detection_single_ts_results_json(dataset, ts_id, df_with_class_instances, scores, y_hat_results, settings):
    data = {}
    data_series = []

    df_z = df_zscore(df_with_class_instances.drop('class', axis=1))
    df_z_with_class_instances = df_z.join(df_with_class_instances['class'])

    corr_time_series = dataset.timeseries_set.all().exclude(id=ts_id)
    ts = TimeSeries.objects.get(id=ts_id)

    # ts
    raw_measurements = get_predicted_series_data_json(ts.id, df_with_class_instances, scores, y_hat_results, settings)
    z_measurements = get_predicted_series_data_json(ts.id, df_z_with_class_instances, scores, y_hat_results, settings)

    dict_series = {'id': ts.id, 'name': ts.name, 'unit': ts.unit, 'is_spatial': ts.is_spatial(),
                   'measurements': {'raw': raw_measurements, 'zscore': z_measurements}}
    data_series.append(dict_series)

    #correlated ts
    for corr_ts in corr_time_series:
        raw_measurements = get_data_series_measurements(corr_ts.id, df_with_class_instances.drop('class', axis=1), y_hat_results)
        z_measurements = get_data_series_measurements(corr_ts.id, df_z, y_hat_results)

        dict_series = {'id': corr_ts.id, 'name': corr_ts.name, 'unit': corr_ts.unit, 'is_spatial': corr_ts.is_spatial(),
                       'measurements': {'raw': raw_measurements, 'zscore': z_measurements}}
        data_series.append(dict_series)

    data['series'] = data_series

    return data


def get_anomaly_detection_results_json(dataset, df_with_class_instances, scores, y_hat_results, settings):
    data = []
    time_series = dataset.timeseries_set.all()

    for ts in time_series:
        data_series = get_predicted_series_data_json(ts.id, df_with_class_instances, scores, y_hat_results, settings)

        dict_series = {'id' : ts.id,
                       'name' : ts.name, #todo
                       'unit' : ts.unit, #todo
                       'is_spatial' : ts.is_spatial(), #todo
                       'type' : 'raw', #todo
                       'data' : data_series
                       }

        data.append(dict_series)

    return data


def _set_marker_for_threshold(point, threshold, settings, upper_boundary=False):
    """
    :param point:
    :param threshold:
    :param settings:
    :param upper_boundary: determines if score higher than thresholds are anomalies or not
    """
    if upper_boundary:
        if point['class'] == 1 and point['score'] > threshold: #true positive
            point['marker'] = {'fillColor': settings['color_true_positive'], 'radius': 3}
        elif point['class'] == 1 and point['score'] <= threshold: #false negative
            point['marker'] = {'fillColor': settings['color_false_negative'], 'radius': 3}
        elif point['class'] == 0 and point['score'] > threshold:  #false positive
            point['marker'] = {'fillColor': settings['color_false_positive'], 'radius': 3}
        elif point['class'] == 0 and point['score'] <= threshold:  # true negative
            point['marker'] = {'enabled': False }

    else:
        if point['class'] == 1 and point['score'] < threshold: #true positive
            point['marker'] = {'fillColor': settings['color_true_positive'], 'radius': 3}
        elif point['class'] == 1 and point['score'] >= threshold: #false negative
            point['marker'] = {'fillColor': settings['color_false_negative'], 'radius': 3}
        elif point['class'] == 0 and point['score'] < threshold:  #false positive
            point['marker'] = {'fillColor': settings['color_false_positive'], 'radius': 3}
        elif point['class'] == 0 and point['score'] >= threshold:  # true negative
            point['marker'] = {'enabled': False }



def _get_scores_and_truth_from_series_data(series_data):
    scores = []
    truth = []
    for point in series_data:
        scores.append(point['score'])
        truth.append(point['class'])

    return np.array(scores), np.array(truth)


def get_datasets_from_json(dataset_series):
    
    df_raw = pd.json_normalize(dataset_series['series'], record_path=['data'], meta=['id', 'type'])

    # transform raw df into dataset df and class df
    df = df_raw.pivot(index='x', columns='id', values='y').rename_axis('time', axis=0).rename_axis('ts_name', axis=1)
    df.index = pd.to_datetime(df.index, unit='ms', infer_datetime_format=True)

    df_class = df_raw.pivot(index='x', columns='id', values='class').rename_axis('time', axis=0).rename_axis('ts_name', axis=1)
    df_class.index = pd.to_datetime(df_class.index, unit='ms', infer_datetime_format=True)

    return df, df_class


def get_updated_dataset_series_for_threshold_json(dataset_series, threshold, settings):

    for series in dataset_series['series']:
        for point in series['data']:
            _set_marker_for_threshold(point, threshold, settings)

    # todo if not lisa we detected anomalous instance not point, so points at the same timestamp have the same truth and score
    series_first = dataset_series['series'][0]
    series_first_data = series_first['data']
    scores, truth = _get_scores_and_truth_from_series_data(series_first_data)
    y_hat_results = (scores < threshold).astype(int)
    info = get_info(threshold, y_hat_results, truth)

    return dataset_series, info


@DeprecationWarning
def get_updated_dataset_series_for_threshold_with_marker_json(threshold, dataset_series, info, algorithm, settings):

    for series in dataset_series:
        for measurement in series['measurements']:
            _set_marker_for_threshold(measurement, threshold, settings)

    if algorithm != LISA_PEARSON: #todo if not lisa we detected anomalous instance not point, so points at the same timestamp have the same truth and score
        series_first = dataset_series[0]
        series_first_measurements = series_first['measurements']
        scores, truth = _get_scores_and_truth_from_series_data(series_first_measurements)
        y_hat_results = (scores < threshold).astype(int)
        new_info = get_info(threshold, y_hat_results, truth)
        new_info['thresholds'] = info['thresholds']
        new_info['threshold_scores'] = info['threshold_scores']
    else:
        #todo
        info = {}

    return dataset_series, new_info
