import numpy as np
from django.urls import reverse

from .date_utils import unix_time_millis_from_dt
from vadetisweb.library import df_zscore
from vadetisweb.parameters import REAL_WORLD

@DeprecationWarning
def datatable_dataset_rows(data, datasets):
    for dataset in datasets:
        row = []

        """
        TODO
        if dataset.type == REAL_WORLD:
            link = reverse('vadetisweb:dataset_real_world', args=[dataset.id])
        else:
            link = reverse('vadetisweb:dataset_synthetic', args=[dataset.id])
        """
        link = ""

        np_num_values = dataset.dataframe.count().sum()

        dataset_link = '<a href="%s">%s (%s)</a>' % (link, dataset.title, dataset.id)
        row.append(dataset_link)
        row.append(dataset.owner.username)
        row.append(dataset.timeseries_set.count())
        row.append(int(np_num_values) if isinstance(np_num_values,
                                                    np.integer) else np_num_values)  # numpy int32/64 is not json serializable
        row.append(dataset.frequency)
        row.append(dataset.type_of_data)
        row.append(dataset.spatial_data)
        row.append(dataset.training_dataset.count())

        data.append(row)

    return data


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
