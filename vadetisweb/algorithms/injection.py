import random
import numpy as np

from .injector.extreme_value_injector import ExtremeValueInjector
from .injector.level_shift_injector import LevelShiftInjector
from .injector.trend_injector import TrendInjector
from .injector.variance_injector import VarianceInjector

from vadetisweb.utils import stochastic_duration
from vadetisweb.utils import next_earlier_dt, next_later_dt, get_datasets_from_json
from vadetisweb.parameters import ANOMALY_TYPE_EXTREME, ANOMALY_TYPE_LEVEL_SHIFT, ANOMALY_TYPE_VARIANCE, ANOMALY_TYPE_TREND

def anomaly_injection(validated_data):

    anomaly_type = validated_data['anomaly_type']

    if anomaly_type == ANOMALY_TYPE_EXTREME:
        injector = ExtremeValueInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_LEVEL_SHIFT:
        injector = LevelShiftInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_TREND:
        injector = TrendInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_VARIANCE:
        injector = VarianceInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    df_from_json, df_class_from_json = get_datasets_from_json(validated_data['dataset_series_json'])
    return df_from_json, df_class_from_json



def deprecated_inject_extreme_outliers(df, df_inject, df_inject_class, anomaly_start_index, normal_start_index, ts_id, factor=10):
    for index, value in df.loc[df.index[anomaly_start_index:normal_start_index], ts_id].iteritems():
        df_inject.at[index, ts_id] = deprecated_extreme_outlier(df, index, ts_id, factor)
        df_inject_class.at[index, ts_id] = 1


def deprecated_extreme_outlier(df, index, ts_id, factor=10):
    before_dt = next_earlier_dt(index, df.index.inferred_freq, 10)
    after_dt = next_later_dt(index, df.index.inferred_freq, 10)
    local_std = df.loc[before_dt:after_dt, ts_id].std(axis=0, skipna=True, level=None, ddof=0)
    return np.random.choice([-1, 1]) * factor * local_std


def deprecated_inject_level_shift(df, df_inject, df_inject_class, anomaly_start_index, normal_start_index, ts_id, factor=10):
    before_dt = next_earlier_dt(df.index[anomaly_start_index], df.index.inferred_freq, 10)
    after_dt = next_later_dt(df.index[normal_start_index], df.index.inferred_freq, 10)
    local_std = df.loc[before_dt:after_dt, ts_id].std(axis=0, skipna=True, level=None, ddof=0)

    multiplier = np.random.choice([-1, 1])
    for index, value in df.loc[df.index[anomaly_start_index:normal_start_index], ts_id].iteritems():
        df_inject.at[index, ts_id] += multiplier * factor * local_std
        df_inject_class.at[index, ts_id] = 1


