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

    normal_lower = validated_data['normal_range']['lower']
    normal_upper = validated_data['normal_range']['upper']
    probability = validated_data['probability']
    anomaly_lower = validated_data['anomaly_range']['lower']
    anomaly_upper = validated_data['anomaly_range']['upper']

    done = False
    normal_start_index = 0
    anomaly_start_index = 0

    while done is False:
        normal_duration = stochastic_duration(normal_lower, normal_upper)
        anomaly_duration = stochastic_duration(anomaly_lower, anomaly_upper)

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


