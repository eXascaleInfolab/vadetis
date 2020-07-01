import numpy as np
import logging, random

from .base import OutlierInjector

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

        #local_std = self.df_from_json.loc[max(index_min, before_dt):min(after_dt, index_max), ts_id].std(axis=0, skipna=True, level=None, ddof=0)
        injection_series = self.df.loc[lower_boundary:upper_boundary, ts_id]

        # remove indexes which are already an anomaly, we won't consider them for the deviation value as it would change the outcome significantly
        anomaly_indexes = []
        for index, value in self.df_class.loc[injection_series.index, ts_id].iteritems():
            if value == True:
                anomaly_indexes.append(index)
        injection_series.drop(index=anomaly_indexes)

        # check the remaining length
        if injection_series.index.size == 0:
            logging.warning("Cannot compute an anomaly in a range that contains only anomalies")
            return 0

        local_std = injection_series.std(axis=0, skipna=True, level=None, ddof=0)
        return np.random.choice([-1, 1]) * self.get_factor() * local_std

    def inject_outliers(self):
        ts_id = self.get_time_series().id
        inject_at_index = random.choice(self.get_range_indexes_dt())
        addition = self.get_value(inject_at_index, ts_id)
        print("addition: ", addition)
        self.df_inject.at[inject_at_index, ts_id] += self.get_value(inject_at_index, ts_id)
        self.df_inject_class.at[inject_at_index, ts_id] = 1
