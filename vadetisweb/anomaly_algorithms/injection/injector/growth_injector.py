import numpy as np, pandas as pd
import logging

from .base import OutlierInjector

from vadetisweb.parameters import *
from vadetisweb.utils import next_earlier_dt, next_later_dt
from vadetisweb.factory import msg_injection_all_anomalies


class GrowthInjector(OutlierInjector):

    def __init__(self, validated_data):
        super().__init__(validated_data)

    def get_factor(self):
        factor = super().get_factor()
        return factor / 10 # adjustment for growth

    def get_split_ranges(self):
        """
        For growth we consider only every second range in order to have some space between subsequent trends
        :return: the ranges to insert the anomaly into
        """
        split_ranges = super().get_split_ranges()
        return split_ranges[1:len(split_ranges):2] if len(split_ranges) > 1 else split_ranges # numpy [start:stop:step]

    def inject(self, range):
        ts_id = self.get_time_series().id
        inject_at_index = self.next_injection_index(range)
        if inject_at_index is not None:

            upper_boundary = min(next_later_dt(inject_at_index, self.df.index.inferred_freq, 10), self.df.index.max())
            growth_indexes = pd.date_range(inject_at_index, upper_boundary, freq=self.df.index.inferred_freq)
            slope = np.random.choice([-1, 1]) * self.get_factor() * np.arange(len(growth_indexes))

            # trend
            self.df_inject.loc[growth_indexes, ts_id] += slope
            self.df_inject_class.loc[growth_indexes, ts_id] = 1

            # adjust remaining
            self.df_inject.loc[self.df_inject.index > upper_boundary, ts_id] += slope[-1]