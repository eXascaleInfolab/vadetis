import numpy as np
import pandas as pd

from vadetisweb.utils import next_earlier_dt, next_later_dt
from .base import OutlierInjector


class DistortionInjector(OutlierInjector):

    def __init__(self, validated_data):
        super().__init__(validated_data)

    def get_split_ranges(self):
        """
        For distortion we consider only every second range in order to have some space between subsequent distortions
        :return: the ranges to insert the anomaly into
        """
        split_ranges = super().get_split_ranges()
        return split_ranges[1:len(split_ranges):2] if len(split_ranges) > 1 else split_ranges # numpy [start:stop:step]

    def inject(self, range):
        ts_id = self.get_time_series().id
        inject_at_index = self.next_injection_index(range)
        if inject_at_index is not None:

            lower_boundary_before = max(next_earlier_dt(inject_at_index, self.df.index.inferred_freq, 5), self.df.index.min())

            if lower_boundary_before == self.df.index.min():
                lower_boundary = next_later_dt(lower_boundary_before, self.df.index.inferred_freq, 1)
            else:
                lower_boundary = max(next_earlier_dt(inject_at_index, self.df.index.inferred_freq, 4), self.df.index.min())

            upper_boundary = min(next_later_dt(inject_at_index, self.df.index.inferred_freq, 5), self.df.index.max())

            variance_diff_indexes = pd.date_range(lower_boundary_before, upper_boundary, freq=self.df.index.inferred_freq)
            variance_indexes = pd.date_range(lower_boundary, upper_boundary, freq=self.df.index.inferred_freq)

            difference = np.diff(self.df.loc[variance_diff_indexes, ts_id])

            # distortion
            self.df_inject.loc[variance_indexes, ts_id] += (self.get_factor() - 1) * difference
            self.df_inject_class.loc[variance_indexes, ts_id] = 1