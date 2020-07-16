
from vadetisweb.anomaly_algorithms.injection import *
from vadetisweb.utils import get_datasets_from_json
from vadetisweb.parameters import ANOMALY_TYPE_POINT, ANOMALY_TYPE_AMPLITUDE_SHIFT, ANOMALY_TYPE_DISTORTION, ANOMALY_TYPE_GROWTH_CHANGE

def anomaly_injection(validated_data):

    anomaly_type = validated_data['anomaly_type']

    if anomaly_type == ANOMALY_TYPE_POINT:
        injector = ExtremeValueInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_AMPLITUDE_SHIFT:
        injector = AmplitudeShiftInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_GROWTH_CHANGE:
        injector = GrowthInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    elif anomaly_type == ANOMALY_TYPE_DISTORTION:
        injector = DistortionInjector(validated_data)
        injector.inject_outliers()
        return injector.get_injection_datasets()

    else:
        logging.error("Unknown anomaly type, will return original datasets")
        df_from_json, df_class_from_json = get_datasets_from_json(validated_data['dataset_series_json'])
        return df_from_json, df_class_from_json
