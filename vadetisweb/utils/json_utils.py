from .date_utils import unix_time_millis_from_dt
from vadetisweb.library import df_zscore


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
        for index, value in df.loc[:, ts.name].iteritems():
            if not show_anomaly:
                measurements.append({'x': unix_time_millis_from_dt(index), 'y': value})
            else:
                df_class = dataset.dataframe_class
                outlier_color = settings['color_outliers']

                if df_class.loc[index, ts.name] == False:
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
