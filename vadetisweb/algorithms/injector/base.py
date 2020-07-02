import random, logging

from vadetisweb.utils import get_datasets_from_json, unix_time_millis_to_dt
from vadetisweb.parameters import *
from vadetisweb.factory import warning_msg_injection_all_anomalies

class OutlierInjector:

    def __init__(self, validated_data):
        self.validated_data = validated_data
        self._set_datasets()

    def _set_datasets(self):
        self.df, self.df_class = self._extract_datasets()
        self.df_inject = self.df.copy()
        self.df_inject_class = self.df_class.copy()

    def _extract_datasets(self):
        df_from_json, df_class_from_json = get_datasets_from_json(self.validated_data['dataset_series_json'])
        return df_from_json, df_class_from_json

    def get_datasets(self):
        return self.df, self.df_class

    def get_injection_datasets(self):
        return self.df_inject, self.df_inject_class

    def get_range_start_dt(self):
        return unix_time_millis_to_dt(self.validated_data['range_start'])

    def get_range_end_dt(self):
        return unix_time_millis_to_dt(self.validated_data['range_end'])

    def get_time_series(self):
        return self.validated_data['time_series']

    def get_range_indexes_dt(self):
        return self.df.loc[self.get_range_start_dt():self.get_range_end_dt()].index.tolist()

    def valid_time_range(self):
        """
        If a time range fr a time series consists only of anomalies, its not valid, as there is not possibility to inject an anomaly
        :return:
        """
        ts_id = self.get_time_series().id
        if self.df_class.loc[self.get_range_indexes_dt(), ts_id].eq(True).all():
            logging.warning(warning_msg_injection_all_anomalies())
            return False
        else:
            return True

    def get_factor(self):
            anomaly_deviation = self.validated_data['anomaly_deviation']
            if anomaly_deviation == ANOMALY_INJECTION_DEVIATION_SMALL:
                return 8

            elif anomaly_deviation == ANOMALY_INJECTION_DEVIATION_MEDIUM:
                return 12

            elif anomaly_deviation == ANOMALY_INJECTION_DEVIATION_HIGH:
                return 16

            elif anomaly_deviation == ANOMALY_INJECTION_DEVIATION_RANDOM:
                return random.choice([8, 12, 16])
            else:
                raise ValueError

    def next_injection_index(self):
        return NotImplementedError

    def inject(self):
        return NotImplementedError

    def inject_outliers(self):
        if self.valid_time_range():
            self.inject()
