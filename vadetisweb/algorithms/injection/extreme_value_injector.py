import numpy as np

from .base import OutlierInjector


class ExtremeValueInjector(OutlierInjector):

    def __init__(self, df_indexes, validated_data):
        super().__init__(df_indexes, validated_data)
        self.timestamps = [] if timestamps is None else list(sum(timestamps, ()))


    def get_value(self, index, timeseries):
        if index in self.timestamps:
            local_std = timeseries.iloc[max(0, index - 10):index + 10].std()
            return np.random.choice([-1, 1]) * self.get_factor() * local_std
        else:
            return 0

    def add_outliers(self, df_indexes):
        additional_values = []
        for timestamp_index in range(len(df_indexes)):
            additional_values.append(self.get_value(timestamp_index, df_indexes))
        return additional_values