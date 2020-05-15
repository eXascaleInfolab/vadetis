import random
import numpy as np

from vadetisweb.utils import stochastic_duration
from vadetisweb.utils import next_dt
from vadetisweb.parameters import ANOMALY_TYPE_EXTREME, ANOMALY_TYPE_LEVEL_SHIFT, ANOMALY_TYPE_VARIANCE, ANOMALY_TYPE_TREND

def anomaly_injection(dataset, validated_data):

    df = dataset.dataframe
    df_class = dataset.dataframe_class

    df_inject = dataset.dataframe.copy()
    df_inject_class = dataset.dataframe_class.copy()
    #time_series = dataset.timeseries_set.all()

    time_series = validated_data['time_series']
    anomaly_type = validated_data['anomaly_type']
    anomaly_factor = validated_data['anomaly_factor']
    normal_lowerbound_duration = validated_data['normal_lowerbound_duration']
    normal_upperbound_duration = validated_data['normal_upperbound_duration']
    probability = validated_data['probability']
    anomaly_lowerbound_duration = validated_data['anomaly_lowerbound_duration']
    anomaly_upperbound_duration = validated_data['anomaly_upperbound_duration']


    done = False
    normal_start_index = 0
    anomaly_start_index = 0

    while done is False:
        normal_duration = stochastic_duration(normal_lowerbound_duration, normal_upperbound_duration)
        anomaly_duration = stochastic_duration(anomaly_lowerbound_duration, anomaly_upperbound_duration)

        # start of next anomaly duration
        anomaly_start_index += normal_start_index + normal_duration
        # start of next normal duration
        normal_start_index += anomaly_start_index + anomaly_duration

        # check break
        if len(df.index) < anomaly_start_index:
            done = True
        else:
            # respect probability
            if random.uniform(0, 1) <= probability:

                if anomaly_type == ANOMALY_TYPE_EXTREME:
                    inject_extreme_outliers(df, df_inject, df_inject_class, anomaly_start_index, normal_start_index, time_series.id, anomaly_factor)

                elif anomaly_type == ANOMALY_TYPE_LEVEL_SHIFT:
                    inject_level_shift(df, df_inject, df_inject_class, anomaly_start_index, normal_start_index, time_series.id, anomaly_factor)

                """elif anomaly_type == ANOMALY_TYPE_VARIANCE:

                elif anomaly_type == ANOMALY_TYPE_TREND:"""



                #inject_correlated_std_deviation_anomaly(df, df_inject, df_inject_class, index, time_series.id)

    return df_inject, df_inject_class

def inject_extreme_outliers(df, df_inject, df_inject_class, anomaly_start_index, normal_start_index, ts_id, factor=10):
    for index, value in df.loc[df.index[anomaly_start_index:normal_start_index], ts_id].iteritems():
        df_inject.at[index, ts_id] = extreme_outlier(df, index, ts_id, factor)
        df_inject_class.at[index, ts_id] = True

def extreme_outlier(df, index, ts_id, factor=10):
    before_dt = next_dt(index, 'earlier', df.index.inferred_freq, 10)
    after_dt = next_dt(index, 'later', df.index.inferred_freq, 10)
    local_std = df.loc[before_dt:after_dt, ts_id].std(axis=0, skipna=True, level=None, ddof=0)
    return np.random.choice([-1, 1]) * factor * local_std

def inject_level_shift(df, df_inject, df_inject_class, anomaly_start_index, normal_start_index, ts_id, factor=10):
    before_dt = next_dt(df.index[anomaly_start_index], 'earlier', df.index.inferred_freq, 10)
    after_dt = next_dt(df.index[normal_start_index], 'later', df.index.inferred_freq, 10)
    local_std = df.loc[before_dt:after_dt, ts_id].std(axis=0, skipna=True, level=None, ddof=0)

    multiplier = np.random.choice([-1, 1])
    for index, value in df.loc[df.index[anomaly_start_index:normal_start_index], ts_id].iteritems():
        df_inject.at[index, ts_id] += multiplier * factor * local_std
        df_inject_class.at[index, ts_id] = True


@DeprecationWarning
def inject_correlated_std_deviation_anomaly(df, df_inject, df_inject_class, index, ts_id, multiplier=3):
    df_inject_class.at[index, ts_id] = True
    # ddof = 0: population standard deviation using n; ddof = 1: sample std deviation using n-1
    std_deviation = df.loc[index,:].std(axis=0, skipna=True, level=None, ddof=0)
    multi = multiplier * -1 if random.randint(0,100) <= 50 else multiplier
    anomaly = (multi * std_deviation) + df.at[index, ts_id]
    df_inject.at[index, ts_id] = anomaly


class MultivariateExtremeOutlierGenerator():
    def __init__(self, timestamps=None, factor=8):
        self.timestamps = [] if timestamps is None else list(sum(timestamps, ()))
        self.factor = factor

    def get_value(self, current_timestamp, timeseries):
        if current_timestamp in self.timestamps:
            local_std = timeseries.iloc[max(0, current_timestamp - 10):current_timestamp + 10].std()
            return np.random.choice([-1, 1]) * self.factor * local_std
        else:
            return 0

    def add_outliers(self, timeseries):
        additional_values = []
        for timestamp_index in range(len(timeseries)):
            additional_values.append(self.get_value(timestamp_index, timeseries))
        return additional_values
