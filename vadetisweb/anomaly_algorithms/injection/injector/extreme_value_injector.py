import numpy as np
import logging

from .base import OutlierInjector

from vadetisweb.parameters import *
from vadetisweb.factory import msg_injection_all_anomalies
from vadetisweb.utils import next_earlier_dt, next_later_dt

class ExtremeValueInjector(OutlierInjector):

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


    def inject(self, range):
        ts_id = self.get_time_series().id
        inject_at_index = self.next_injection_index(range)
        if inject_at_index is not None:
            adjustment_value = self.get_value(inject_at_index, ts_id)
            if adjustment_value != 0:
                self.df_inject.at[inject_at_index, ts_id] += adjustment_value
                self.df_inject_class.at[inject_at_index, ts_id] = 1
