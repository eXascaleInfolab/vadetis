
from vadetisweb.anomaly_algorithms.injection import *
from vadetisweb.utils import get_datasets_from_json
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

    else:
        logging.error("Unknown anomaly type, will return original datasets")
        df_from_json, df_class_from_json = get_datasets_from_json(validated_data['dataset_series_json'])
        return df_from_json, df_class_from_json
