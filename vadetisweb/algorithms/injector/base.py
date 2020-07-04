import numpy as np
import logging

from vadetisweb.parameters import *
from vadetisweb.utils import get_datasets_from_json, unix_time_millis_to_dt
from vadetisweb.factory import warning_msg_injection_all_anomalies

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

    def _number_of_splits(self):
        anomaly_deviation = self.validated_data['anomaly_repetition']
        if anomaly_deviation == ANOMALY_INJECTION_REPEAT_INTERVAL_LOW:
            return 4

        elif anomaly_deviation == ANOMALY_INJECTION_REPEAT_INTERVAL_MEDIUM:
            return 8

        elif anomaly_deviation == ANOMALY_INJECTION_REPEAT_INTERVAL_HIGH:
            return 16

        elif anomaly_deviation == ANOMALY_INJECTION_REPEAT_SINGLE:
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

    def valid_time_range(self, range_indexes):
        """
        If a time range for a time series consists only of anomalies, its not valid, as there is not possibility to inject an anomaly
        :return:
        """
        ts_id = self.get_time_series().id
        if self.df_class.loc[range_indexes, ts_id].eq(True).all():
            logging.warning(warning_msg_injection_all_anomalies())
            return False
        else:
            return True

    def get_factor(self):
        return NotImplementedError

    def next_injection_index(self, range):
        return NotImplementedError

    def inject(self, range):
        return NotImplementedError

    def inject_outliers(self):
        if self.valid_time_range(range_indexes=self.get_range_indexes_dt()):
            self.splitted_ranges = self.split(self.df.loc[self.get_range_start_dt():self.get_range_end_dt()].index, self._number_of_splits())
            for range in self.splitted_ranges:
                self.inject(range)