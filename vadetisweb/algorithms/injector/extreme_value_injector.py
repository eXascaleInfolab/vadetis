import numpy as np
import logging, random

from .base import OutlierInjector

from vadetisweb.factory import warning_msg_injection_all_anomalies
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

        frequency = self.df.index.inferred_freq
        before_dt = next_earlier_dt(inject_at_index, frequency, 10)
        after_dt = next_later_dt(inject_at_index, frequency, 10)

        index_min = self.df.index.min()
        index_max = self.df.index.max()

        lower_boundary = max(index_min, before_dt)
        upper_boundary = min(after_dt, index_max)

        injection_series = self.df.loc[lower_boundary:upper_boundary, ts_id]

        # remove indexes which are already an anomaly, we won't consider them for the deviation value as it would change the outcome significantly
        anomaly_indexes = []
        for index, value in self.df_class.loc[injection_series.index, ts_id].iteritems():
            if value == True:
                anomaly_indexes.append(index)
        injection_series = injection_series.drop(index=anomaly_indexes)

        # check the remaining length
        if injection_series.index.size == 0:
            logging.warning(warning_msg_injection_all_anomalies())
            return 0

        local_std = injection_series.std(axis=0, skipna=True, level=None, ddof=0)
        return np.random.choice([-1, 1]) * self.get_factor() * local_std


    def next_injection_index(self):
        """
        Is only safe to be called after valid_time_range
        :return: next index to insert anomaly
        """
        ts_id = self.get_time_series().id
        inject_at_index = random.choice(self.get_range_indexes_dt())
        if self.df_class.loc[inject_at_index, ts_id] == True:
            return self.next_injection_index()
        else:
            return inject_at_index


    def inject_outliers(self):
        if self.valid_time_range():
            ts_id = self.get_time_series().id
            inject_at_index = self.next_injection_index()
            addition = self.get_value(inject_at_index, ts_id)
            logging.debug("addition: ", addition)
            self.df_inject.at[inject_at_index, ts_id] += addition
            self.df_inject_class.at[inject_at_index, ts_id] = 1
