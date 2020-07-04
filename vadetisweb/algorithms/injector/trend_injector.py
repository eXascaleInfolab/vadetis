import numpy as np, pandas as pd
import logging

from .base import OutlierInjector

from vadetisweb.parameters import *
from vadetisweb.utils import next_earlier_dt, next_later_dt
from vadetisweb.factory import msg_injection_all_anomalies


class TrendInjector(OutlierInjector):

    def __init__(self, validated_data):
        super().__init__(validated_data)

    def get_factor(self):
        anomaly_deviation = self.validated_data['anomaly_deviation']
        if anomaly_deviation == ANOMALY_INJECTION_DEVIATION_SMALL:
            return 8 / 10

        elif anomaly_deviation == ANOMALY_INJECTION_DEVIATION_MEDIUM:
            return 16 / 10

        elif anomaly_deviation == ANOMALY_INJECTION_DEVIATION_HIGH:
            return 24 / 10

        elif anomaly_deviation == ANOMALY_INJECTION_DEVIATION_RANDOM:
            return np.random.choice([8 / 10, 16 / 10, 24 / 10])

        else:
            raise ValueError

    def next_injection_index(self, range):
        """
        :param range - the range in which the anomaly is injected
        :return: next index to insert anomaly
        """
        if self.valid_time_range(range_indexes=range):
            ts_id = self.get_time_series().id
            df_normal_part = self.df_class.loc[(self.df_class.index.isin(range)) & (self.df_class[ts_id] == False), ts_id]
            normal_indexes = df_normal_part.index
            inject_at_index = np.random.choice(normal_indexes)
            return inject_at_index

        return None

    def get_split_ranges(self):
        """
        For trend we consider only every second range in order to have some space between subsequent trends
        :return: the ranges to insert the anomaly into
        """
        split_ranges = super().get_split_ranges()
        return split_ranges[1:len(split_ranges):2] if len(split_ranges) > 1 else split_ranges # numpy [start:stop:step]

    def inject(self, range):
        ts_id = self.get_time_series().id
        inject_at_index = self.next_injection_index(range)
        if inject_at_index is not None:

            upper_boundary = min(next_later_dt(inject_at_index, self.df.index.inferred_freq, 10), self.df.index.max())
            trend_indexes = pd.date_range(inject_at_index, upper_boundary, freq=self.df.index.inferred_freq)
            slope = np.random.choice([-1, 1]) * self.get_factor() * np.arange(len(trend_indexes))

            # trend
            self.df_inject.loc[trend_indexes, ts_id] += slope
            self.df_inject_class.loc[trend_indexes, ts_id] = 1

            # adjust remaining
            self.df_inject.loc[self.df_inject.index > upper_boundary, ts_id] += slope[-1]