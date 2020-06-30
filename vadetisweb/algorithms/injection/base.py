
from vadetisweb.utils import get_datasets_from_json
from vadetisweb.parameters import ANOMALY_INJECTION_REPEAT_INTERVAL_LOW, ANOMALY_INJECTION_REPEAT_INTERVAL_MEDIUM, ANOMALY_INJECTION_REPEAT_INTERVAL_HIGH


class OutlierInjector:

    def __init__(self, df_indexes, validated_data):
        self._set_datasets()
        self.df_indexes = df_indexes
        self.validated_data = validated_data

    def _set_datasets(self):
        self.df_from_json, self.df_class_from_json = self.get_datasets()
        self.df_inject = self.df_from_json.copy()
        self.df_inject_class = self.df_class_from_json.copy()

    def get_datasets(self):
        df_from_json, df_class_from_json = get_datasets_from_json(self.validated_data['dataset_series_json'])
        return df_from_json, df_class_from_json

    def get_range_start(self):
        return self.validated_data['range_start']

    def get_range_end(self):
        return self.validated_data['range_end']

    #def get_range_indexes(self):


    def get_factor(self):
        anomaly_deviation = self.validated_data['anomaly_deviation']
        if anomaly_deviation == ANOMALY_INJECTION_REPEAT_INTERVAL_LOW:
            return 4

        elif anomaly_deviation == ANOMALY_INJECTION_REPEAT_INTERVAL_MEDIUM:
            return 8

        elif anomaly_deviation == ANOMALY_INJECTION_REPEAT_INTERVAL_HIGH:
            return 12

        else:
            raise ValueError

    def inject_outliers(self, df_indexes):
        return NotImplementedError