import logging

import numpy as np
import pandas as pd

from vadetisweb.factory import msg_injection_all_anomalies
from vadetisweb.utils import next_earlier_dt, next_later_dt
from .base import OutlierInjector


class AmplitudeShiftInjector(OutlierInjector):

    def __init__(self, validated_data):
        super().__init__(validated_data)

    def get_value(self, inject_at_index, ts_id):
        """
        :param inject_at_index: the index to inject the anomaly at
        :param ts_id: the affected time series
        :return: the value to add to the current value at index 'inject_at_index'
        """

        frequency = self.df.index.inferred_freq # the granularity
        before_dt = next_earlier_dt(inject_at_index, frequency, 10)
        after_dt = next_later_dt(inject_at_index, frequency, 10)

        index_min = self.df.index.min()
        index_max = self.df.index.max()

        lower_boundary = max(index_min, before_dt)
        upper_boundary = min(after_dt, index_max)

        injection_series = self.df.loc[lower_boundary:upper_boundary, ts_id]

        # remove indexes which are already an anomaly, we won't consider them for the deviation value as it would change the outcome significantly
        df_anomaly_part = self.df_class.loc[(self.df_class.index.isin(injection_series.index)) & (self.df_class[ts_id] == True), ts_id]
        injection_series = injection_series.drop(index=df_anomaly_part.index)

        # check the remaining length
        if injection_series.index.size == 0:
            logging.debug(msg_injection_all_anomalies())
            return 0

        local_std = injection_series.std(axis=0, skipna=True, level=None, ddof=0)
        return np.random.choice([-1, 1]) * self.get_factor() * local_std


    def get_split_ranges(self):
        """
        For amplitude shift we consider only every second range in order to have some space between subsequent level shifts
        :return: the ranges to insert the anomaly into
        """
        split_ranges = super().get_split_ranges()
        return split_ranges[1:len(split_ranges):2] if len(split_ranges) > 1 else split_ranges # numpy [start:stop:step]


    def inject(self, range_index):
        ts_id = self.get_time_series().id
        inject_at_index = self.next_injection_index(range_index)
        if inject_at_index is not None:

            lower_boundary = max(next_earlier_dt(inject_at_index, self.df.index.inferred_freq, 4), self.df.index.min())
            upper_boundary = min(next_later_dt(inject_at_index, self.df.index.inferred_freq, 5), self.df.index.max())

            level_shift_indexes = pd.date_range(lower_boundary, upper_boundary, freq=self.df.index.inferred_freq)
            adjustment_value = self.get_value(inject_at_index, ts_id)
            if adjustment_value != 0:
                self.df_inject.loc[level_shift_indexes, ts_id] += adjustment_value
                self.df_inject_class.loc[level_shift_indexes, ts_id] = 1