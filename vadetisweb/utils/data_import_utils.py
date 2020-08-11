import collections
import logging

import numpy as np
import pandas as pd
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from vadetisweb.anomaly_algorithms.detection.helper_functions import df_anomaly_instances
from vadetisweb.models import User, Location, TimeSeries, DataSet
from .date_utils import iso_format_time


def _get_supported_granularities():
    return ['AS', 'BYS', 'MS', 'W', 'D', 'H', 'T', 'min', 'S', 'L', 'ms']


def import_dataset(owner_username, dataset_file_name, title, type, **kwargs):
    """
    The execution method of this task. We read the csv with the pandas lib, it's fast!

    :param owner_username: the owner of the dataset
    :param dataset_file_name: CSV file name of the time series
    :param title: Human readable title of the dataset
    :param type: real world or synthetic
    :param kwargs: provide kwarg 'spatial_file_name' when inserting spatial data
    :return: results of the tasks as json
    """

    # set start time
    start_time = timezone.now()

    dataset_csv_name = dataset_file_name

    if 'spatial_file_name' in kwargs:
        spatial_csv_name = kwargs['spatial_file_name']
    else:
        spatial_csv_name = None

    user = User.objects.get(username=owner_username)

    # import time series
    with open(dataset_csv_name, 'r') as file_csv, transaction.atomic():

        # get flatten df
        df_read = pd.read_csv(file_csv,
                              sep=';',
                              parse_dates=['time'],
                              infer_datetime_format=True,
                              index_col='time',
                              float_precision='high')

        # check number of values (row counts)
        num_values = df_read['value'].shape[0]
        if num_values > settings.DATASET_MAX_VALUES:
            raise ValueError("Dataset exceeds value limit {} ({} values provided)".format(settings.DATASET_MAX_VALUES, num_values))

        # check each series must have same unit
        group_by_ts_name = df_read.groupby('ts_name')
        df_ts_unit = group_by_ts_name.apply(lambda x: x['unit'].unique())

        for idx, row in df_ts_unit.items():  # check length of units at each series must be 1
            if not len(row) == 1:
                err_msg = "Series '{0}' has multiple units".format(idx)
                raise ValueError(err_msg)

        df_ts_name = df_read['ts_name'].unique()
        if len(df_ts_name) == 1:  # check length series names must not be 1
            err_msg = "Only one series '{0}' provided. You must include at least 2 time series.".format(idx)
            raise ValueError(err_msg)

        # check each series distinct name => each series has only one value for a given index
        group_by_index = df_read.groupby(level=0)
        if group_by_index.apply(lambda x: x[
            'ts_name'].duplicated()).any():  # true if any value is true => at least one duplicated index for a time series name
            err_msg = "Duplicated index for a time series found"
            raise ValueError(err_msg)

        # unflatten dataframe
        df = df_read.pivot(columns='ts_name', values='value')

        # check if same frequency (granularity) => pandas can infer a frequency
        freq = df.index.inferred_freq
        if freq is None or (freq not in _get_supported_granularities() and not freq.endswith(tuple(_get_supported_granularities()))):
            err_msg = "Series do not have same granularity"
            raise ValueError(err_msg)

        # get anomaly df
        df_class = df_read.pivot(columns='ts_name', values='class')
        df_class = df_class.applymap(lambda x: True if x == 1 else False)

        # check for NaN values, we need complete data for some algorithms
        if df.isnull().values.any() or df_class.isnull().values.any():
            err_msg = "Some values are missing"
            raise ValueError(err_msg)

        # check if different units
        units = []
        for idx, row in df_ts_unit.items():
            unit = row[0]
            if unit not in units:
                units.append(unit)

        if len(units) > 1:
            raise ValueError('Different types of values provided')

        dataset = DataSet.objects.create(title=title,
                                         owner=user,
                                         type=type,
                                         granularity=freq)
        logging.info("New dataset {0} added".format(dataset))

        # for each series create a time series object
        for idx, row in df_ts_unit.items():
            ts = TimeSeries.objects.create(name=idx,
                                           unit=row[0],  # safe to get single element as previously checked for consistency
                                           )
            logging.debug("New time series: {0} added".format(idx))
            ts.datasets.add(dataset)
            ts.save()
            # replace column in dataframe by time series database id
            df = df.rename(columns={idx: ts.id})

        # localize to UTC
        df.index.tz_localize('UTC')
        df_class.tz_localize('UTC')

        # rename df class before assign
        for idx, row in df_ts_unit.items():
            ts = TimeSeries.objects.get(name=idx,
                                        datasets__id=dataset.id)
            # replace column in dataframe by time series database id
            df_class = df_class.rename(columns={idx: ts.id})

        # set dfs
        dataset.dataframe = df
        dataset.dataframe_class = df_class

        dataset.save()

        if spatial_csv_name is not None:
            with open(spatial_csv_name, 'r') as locations_csv:

                # get location df
                df_loc = pd.read_csv(locations_csv,
                                     sep=';',
                                     index_col='ts_name')

                # check if locations for all series are provided
                ts_dataset = TimeSeries.objects.filter(datasets__id=dataset.id)
                ts_names = ts_dataset.values_list('name', flat=True)
                if not np.all(df_loc.index.isin(ts_names) == True):
                    err_msg = "Some time series are missing in location file: %s " % ', '.join(
                        str(x) for x in df_loc[~df_loc.index.isin(ts_names)].index.values)
                    raise ValueError(err_msg)

                # check if needed columns are present and check if values complete
                required_cols = pd.Series(['l_name', 'latitude', 'longitude'])
                if not required_cols.isin(df_loc.columns).all() or df_loc.loc[df_loc.index.intersection(ts_names)].reindex(ts_names).isnull().values.any():
                    err_msg = "Some required values are missing"
                    raise ValueError(err_msg)

                # for each series create a location object
                for idx, row in df_loc.iterrows():
                    ts = TimeSeries.objects.get(datasets__id=dataset.id, name=idx)
                    l_name = row['l_name']
                    lat = row['latitude']
                    lon = row['longitude']

                    location = Location.objects.create(label=l_name,
                                                       latitude=lat,
                                                       longitude=lon)
                    ts.location = location
                    ts.save()
                    location.save()

    execution_time = iso_format_time(timezone.now() - start_time)
    result = {
        'values': int(df.count().sum()),
        'time_series:': len(df.columns),
        'execution_time': execution_time
    }

    return result


def import_training_dataset(owner_username, main_dataset_id, training_dataset_file_name, title):
    # set start time
    start_time = timezone.now()

    filename = training_dataset_file_name

    user = User.objects.get(username=owner_username)

    # import time series
    with open(filename, 'r') as file_csv, transaction.atomic():

        main_dataset = DataSet.objects.filter(id=main_dataset_id, owner=user).first()
        if main_dataset is None:
            raise ValueError("Main dataset not found")

        # get flatten df
        df_read = pd.read_csv(file_csv,
                              sep=';',
                              parse_dates=['time'],
                              infer_datetime_format=True,
                              index_col='time',
                              float_precision='high')

        # check number of values (row counts)
        num_values = df_read['value'].shape[0]
        if num_values > settings.TRAINING_DATA_MAX_SIZE:
            raise ValueError("Dataset exceeds value limit {} ({} values provided)".format(settings.TRAINING_DATA_MAX_SIZE, num_values))

        elif num_values < settings.TRAINING_DATA_MIN_SIZE:
            raise ValueError("Dataset deceeds value limit {} ({} values provided)".format(settings.TRAINING_DATA_MIN_SIZE, num_values))

        # check each series must have same unit
        group_by_ts_name = df_read.groupby('ts_name')
        df_ts_unit = group_by_ts_name.apply(lambda x: x['unit'].unique())

        for idx, row in df_ts_unit.items():  # check length of units at each series must be 1
            if not len(row) == 1:
                err_msg = "Series {0} has multiple units".format(idx)
                raise ValueError(err_msg)

        # check if all time series from original dataset provided, and not more or less
        ts_names_from_original = TimeSeries.objects.filter(datasets__id=main_dataset_id).values_list('name', flat=True)
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        if not compare(list(ts_names_from_original), df_ts_unit.index.tolist()):
            err_msg = "Either some series are missing or some series are provided that are not in the original dataset."
            raise ValueError(err_msg)

        # check each series distinct name => each series has only one value for a given index
        group_by_index = df_read.groupby(level=0)
        if group_by_index.apply(lambda x: x[
            'ts_name'].duplicated()).any():  # true if any value is true => at least one duplicated index for a time series name
            err_msg = "Duplicated index for a time series found"
            raise ValueError(err_msg)

        # unflatten dataframe
        df = df_read.pivot(columns='ts_name', values='value')

        # check if same frequency (granularity) => pandas can infer a frequency
        freq = df.index.inferred_freq
        if freq is None or (freq not in _get_supported_granularities() and not freq.endswith(tuple(_get_supported_granularities()))) or freq != main_dataset.dataframe.index.inferred_freq:
            err_msg = "Series do not have same granularity"
            raise ValueError(err_msg)

        # get anomaly df
        df_class = df_read.pivot(columns='ts_name', values='class')
        df_class = df_class.applymap(lambda x: True if x == 1 else False)

        df_class_instances = df_anomaly_instances(df_class)
        num_normal_instances = df_class_instances[df_class_instances['class'] == False].shape[0]
        if num_normal_instances < settings.TRAINING_DATASET_MIN_NORMAL:  # check min number of values (row counts)
            raise ValueError("Dataset deceeds normal value limit {} ({} values provided)".format(settings.TRAINING_DATASET_MIN_NORMAL, num_normal_instances))

        num_outlier_instances = df_class_instances[df_class_instances['class'] == True].shape[0]
        if num_outlier_instances < settings.TRAINING_DATASET_MIN_ANOMALIES:  # check min number of anomalous values (row counts)
            raise ValueError("Dataset deceeds outlier limit {} ({} values provided)".format(settings.TRAINING_DATASET_MIN_ANOMALIES, num_outlier_instances))

        # check for NaN values, we need complete data for some algorithms
        if df.isnull().values.any() or df_class.isnull().values.any():
            err_msg = "Some values are missing"
            raise ValueError(err_msg)

        # check if different units
        units = []
        for idx, row in df_ts_unit.items():
            unit = row[0]
            if unit not in units:
                units.append(unit)

        if len(units) > 1:
            raise ValueError('Different types of values provided')

        # create (and saves) training dataset
        training_dataset = DataSet.objects.create(title=title,
                                                  owner=user,
                                                  type=main_dataset.type,
                                                  granularity=freq,
                                                  training_data=True,
                                                  main_dataset=main_dataset)

        logging.info("Test dataset {0} added".format(training_dataset))

        # for each series get the time series object
        for idx, row in df_ts_unit.items():
            ts = TimeSeries.objects.get(name=idx,
                                        datasets__id=main_dataset.id)

            logging.debug("Time series: {0} fetched".format(idx))
            ts.datasets.add(training_dataset)
            ts.save()
            # replace column in dataframe by time series database id
            df = df.rename(columns={idx: ts.id})

        # localize to UTC
        df.index.tz_localize('UTC')
        df_class.tz_localize('UTC')

        # rename df class before assign
        for idx, row in df_ts_unit.items():
            ts = TimeSeries.objects.get(name=idx,
                                        datasets__id=main_dataset.id)
            # replace column in dataframe by time series database id
            df_class = df_class.rename(columns={idx: ts.id})

        # set dfs
        training_dataset.dataframe = df
        training_dataset.dataframe_class = df_class

        training_dataset.save()

    execution_time = iso_format_time(timezone.now() - start_time)
    result = {
        'values': int(df.count().sum()),
        'execution_time': execution_time
    }

    return result
