import logging

import numpy as np

from vadetisweb.factory import msg_injection_all_anomalies
from vadetisweb.parameters import *
from vadetisweb.utils import get_datasets_from_json, unix_time_millis_to_dt


class OutlierInjector:

    def __init__(self, validated_data):
        self.validated_data = validated_data
        self._set_datasets()

    def _set_datasets(self):
        self.df, self.df_class = self._extract_datasets()
        self.df_inject = self.df.copy()
        self.df_inject_class = self.df_class.copy()

    def _extract_datasets(self):
        df_from_json, df_class_from_json = get_datasets_from_json(self.validated_data['dataset_series_json'])
        return df_from_json, df_class_from_json

    def get_datasets(self):
        return self.df, self.df_class

    def get_injection_datasets(self):
        return self.df_inject, self.df_inject_class

    def get_range_start_dt(self):
        return unix_time_millis_to_dt(self.validated_data['range_start'])

    def get_range_end_dt(self):
        return unix_time_millis_to_dt(self.validated_data['range_end'])

    def get_time_series(self):
        return self.validated_data['time_series']

    def get_range_indexes_dt(self):
        return self.df.loc[self.get_range_start_dt():self.get_range_end_dt()].index.tolist()

    def get_factor(self):
        anomaly_scale = self.validated_data['anomaly_scale']
        if anomaly_scale == ANOMALY_INJECTION_SCALE_SMALL:
            return 5

        elif anomaly_scale == ANOMALY_INJECTION_SCALE_MEDIUM:
            return 10

        elif anomaly_scale == ANOMALY_INJECTION_SCALE_HIGH:
            return 15

        elif anomaly_scale == ANOMALY_INJECTION_SCALE_RANDOM:
            return np.random.choice([5, 10, 15])

        else:
            raise ValueError

    def next_injection_index(self, range_index):
        """
        :param range_index the range in which the anomaly is injected
        :return: next index to insert anomaly
        """
        if self.valid_time_range(range_indexes=range_index):
            ts_id = self.get_time_series().id
            df_normal_part = self.df_class.loc[(self.df_class.index.isin(range_index)) & (self.df_class[ts_id] == False), ts_id]
            normal_indexes = df_normal_part.index
            inject_at_index = np.random.choice(normal_indexes)
            return inject_at_index

        return None

    def _number_of_splits(self):
        anomaly_scale = self.validated_data['anomaly_repetition']

        range_length = len(self.df.loc[self.get_range_start_dt():self.get_range_end_dt()].index)
        # 30 values is the minimum range in which we inject anomalies
        if range_length < 30:
            return 1

        max_splits = int(range_length / 30)

        if anomaly_scale == ANOMALY_INJECTION_REPEAT_INTERVAL_LOW:
            return min(4, max_splits)

        elif anomaly_scale == ANOMALY_INJECTION_REPEAT_INTERVAL_MEDIUM:
            return min(8, max_splits)

        elif anomaly_scale == ANOMALY_INJECTION_REPEAT_INTERVAL_HIGH:
            return min(16, max_splits)

        elif anomaly_scale == ANOMALY_INJECTION_REPEAT_SINGLE:
            return 1
        else:
            return ValueError


    def split(self, range, n=4):
        """
        :param range: the range to split into n blocks
        :param n: split to produce n blocks
        :return: A list of sub-arrays
        """
        split = np.array_split(range, n)
        return split


    def get_split_ranges(self):
        return self.split(self.df.loc[self.get_range_start_dt():self.get_range_end_dt()].index, self._number_of_splits())

    def valid_time_range(self, range_indexes):
        """
        If a time range for a time series consists only of anomalies, its not valid, as there is not possibility to inject an anomaly
        :return:
        """
        ts_id = self.get_time_series().id
        if self.df_class.loc[range_indexes, ts_id].eq(True).all():
            logging.warning(msg_injection_all_anomalies())
            return False
        else:
            return True

    def inject(self, range):
        return NotImplementedError

    def inject_outliers(self):
        if self.valid_time_range(range_indexes=self.get_range_indexes_dt()):
            for range in self.get_split_ranges():
                self.inject(range)