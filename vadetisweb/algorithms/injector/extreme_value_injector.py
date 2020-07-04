import numpy as np
import logging

from .base import OutlierInjector

from vadetisweb.parameters import *
from vadetisweb.factory import warning_msg_injection_all_anomalies
from vadetisweb.utils import next_earlier_dt, next_later_dt

class ExtremeValueInjector(OutlierInjector):

    def __init__(self, validated_data):
        super().__init__(validated_data)

    def get_factor(self):
        anomaly_deviation = self.validated_data['anomaly_deviation']
        if anomaly_deviation == ANOMALY_INJECTION_DEVIATION_SMALL:
            return 8

        elif anomaly_deviation == ANOMALY_INJECTION_DEVIATION_MEDIUM:
            return 12

        elif anomaly_deviation == ANOMALY_INJECTION_DEVIATION_HIGH:
            return 16

        elif anomaly_deviation == ANOMALY_INJECTION_DEVIATION_RANDOM:
            return np.random.choice([8, 12, 16])

        else:
            raise ValueError


    def get_value(self, inject_at_index, ts_id):
        """
        :param inject_at_index: the index to inject the anomaly at
        :param ts_id: the affected time series
        :return: the value to add to the current value at index 'inject_at_index'
        """

        frequency = self.df.index.inferred_freq
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
            logging.warning(warning_msg_injection_all_anomalies())
            return 0

        local_std = injection_series.std(axis=0, skipna=True, level=None, ddof=0)
        return np.random.choice([-1, 1]) * self.get_factor() * local_std


    def next_injection_index(self, range):
        """
        :param range the range in which the anomaly is injected
        :return: next index to insert anomaly
        """
        if self.valid_time_range(range_indexes=range):
            ts_id = self.get_time_series().id
            df_normal_part = self.df_class.loc[(self.df_class.index.isin(range)) & (self.df_class[ts_id] == False), ts_id]
            normal_indexes = df_normal_part.index
            inject_at_index = np.random.choice(normal_indexes)
            return inject_at_index

        return None


    def inject(self, range):
        ts_id = self.get_time_series().id
        inject_at_index = self.next_injection_index(range)
        if inject_at_index is not None:
            addition = self.get_value(inject_at_index, ts_id)
            logging.debug("addition: ", addition)
            self.df_inject.at[inject_at_index, ts_id] += addition
            self.df_inject_class.at[inject_at_index, ts_id] = 1
