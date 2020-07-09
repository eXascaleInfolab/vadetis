import numpy as np, pandas as pd

from vadetisweb.models import TimeSeries
from vadetisweb.parameters import LISA_PEARSON

from .anomaly_detection_utils import df_zscore
from .date_utils import unix_time_millis_from_dt
from .anomaly_detection_utils import get_detection_meta


def get_type_from_dataset_json(dataset_json):
    """
    Although a dataset is either of type 'raw' or 'zscore' we store this information redundant in
    highcharts' series.options.custom field for each series as it's the most suitable place for it.
    :param dataset_json: the dataset as json
    :return: the common type of the series
    """
    series = dataset_json['series']
    if len(series) > 0 and all(x == series[0]['type'] for x in [s['type'] for s in series]):
        return series[0]['type']
    raise ValueError('Some series are of different type')


def dataset_to_json(dataset, df, df_class, settings, type):
    data_series = []
    time_series = dataset.timeseries_set.all()

    for ts in time_series:
        data = _get_series_data_json(ts.id, df, df_class, settings)

        dict_series = {
            'id': ts.id,
            'name': ts.name,
            'unit': ts.unit,
            'is_spatial': ts.is_spatial(),
            'type': type,
            'dashStyle': 'Solid',
            'data': data,
        }
        data_series.append(dict_series)

    return data_series


def _get_series_data_json(time_series_id, df, df_class, settings):
    data = []
    outlier_color = settings['color_outliers']
    for index, value in df.loc[:, time_series_id].iteritems():
        anomaly_class = 1 if (df_class.loc[index, time_series_id] == True) else 0

        if anomaly_class == 0:
            data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'class': anomaly_class})
        else:
            data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'class': anomaly_class, 'marker': {'fillColor': outlier_color, 'radius': 3}})

    return data


def get_detection_instance_series_data_json(time_series_id, df_with_class_instances, scores, y_hat_results, settings):

    data = []
    for index, value in df_with_class_instances.loc[:, time_series_id].iteritems():

        integer_index = df_with_class_instances.index.get_loc(index)
        predicted_result = y_hat_results[integer_index]
        score = scores[integer_index]

        class_truth = df_with_class_instances.loc[index, 'class'].astype(int)

        _append_detection_point(data, index, value, score, class_truth, predicted_result, settings)

    return data


def get_detection_single_series_data_json(time_series_id, df, df_class, scores, y_hat_results, settings):
    data = []
    for index, value in df.loc[:, time_series_id].iteritems():

        integer_index = df.index.get_loc(index)
        predicted_result = y_hat_results[integer_index]
        score = scores[integer_index]

        class_truth = df_class.loc[index, time_series_id].astype(int)

        _append_detection_point(data, index, value, score, class_truth, predicted_result, settings)

    return data


def _append_detection_point(data, index, value, score, class_truth, predicted_result, settings):

    if class_truth == 1 and predicted_result == True:  # true positive
        data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': class_truth,
                     'marker': {'fillColor': settings['color_true_positive'], 'radius': 3}})

    elif class_truth == 1 and predicted_result == False:  # false negative
        data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': class_truth,
                     'marker': {'fillColor': settings['color_false_negative'], 'radius': 3}})

    elif class_truth == 0 and predicted_result == True:  # false positive
        data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': class_truth,
                     'marker': {'fillColor': settings['color_false_positive'], 'radius': 3}})

    elif class_truth == 0 and predicted_result == False:  # true negative
        data.append({'x': unix_time_millis_from_dt(index), 'y': value, 'score': score, 'class': class_truth, 'marker': {'enabled': False}})


def get_data_series_measurements(id, df_with_class_instances, y_hat_results):

    measurements = []
    for index, value in df_with_class_instances.loc[:, id].iteritems():
        measurements.append({'x': unix_time_millis_from_dt(index), 'y': value, 'marker': {'radius': 0}})

    return measurements


def get_detection_single_ts_results_json(dataset, df, df_class, time_series_id, scores, y_hat_results, settings, type):
    data = []

    time_series = dataset.timeseries_set.all()
    for ts in time_series:

        if ts.id == time_series_id:
            data_series = get_detection_single_series_data_json(ts.id, df, df_class, scores, y_hat_results, settings)
        else:
            data_series = _get_series_data_json(ts.id, df, df_class, settings)

        dict_series = {
            'id': ts.id,
            'name': ts.name,
            'unit': ts.unit,
            'is_spatial': ts.is_spatial(),
            'type': type,
            'dashStyle': 'Dot' if ts.id == time_series_id else 'Solid',
            'data': data_series,
        }
        data.append(dict_series)

    return data


def get_detection_results_json(dataset, df_with_class_instances, scores, y_hat_results, settings, type):
    data = []
    time_series = dataset.timeseries_set.all()

    for ts in time_series:
        data_series = get_detection_instance_series_data_json(ts.id, df_with_class_instances, scores, y_hat_results, settings)

        dict_series = {
            'id' : ts.id,
            'name' : ts.name,
            'unit' : ts.unit,
            'is_spatial' : ts.is_spatial(),
            'type' : type,
            'dashStyle': 'Solid',
            'data' : data_series,
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


def get_locations_json(timeseries):
    data = {}
    points = []
    locations = []
    for ts in timeseries:
        location = ts.location
        locations.append(location)
        points.append({ 'ts' : ts.name, 'label' : location.label, 'latitude' : location.latitude, 'longitude' : location.longitude })

    center_latitude, center_longitude = _center_of_locations(locations)
    data['meta'] = { 'center_latitude' : center_latitude, 'center_longitude' : center_longitude }
    data['points'] = points
    return data


def _center_of_locations(locations):
    lat = []
    long = []
    for l in locations:
        lat.append(l.latitude)
        long.append(l.longitude)

    center_latitude = sum(lat) / len(lat)
    center_longitude = sum(long) / len(long)
    return center_latitude, center_longitude


def get_updated_dataset_series_for_threshold_json(dataset_series, threshold, settings):

    for series in dataset_series['series']:
        for point in series['data']:
            _set_marker_for_threshold(point, threshold, settings)

    # todo if not lisa we detected anomalous instance not point, so points at the same timestamp have the same truth and score
    series_first = dataset_series['series'][0]
    series_first_data = series_first['data']
    scores, truth = _get_scores_and_truth_from_series_data(series_first_data)
    y_hat_results = (scores < threshold).astype(int)
    info = get_detection_meta(threshold, y_hat_results, truth)

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
        new_info = get_detection_meta(threshold, y_hat_results, truth)
        new_info['thresholds'] = info['thresholds']
        new_info['training_threshold_scores'] = info['training_threshold_scores']
    else:
        #todo
        info = {}

    return dataset_series, new_info
