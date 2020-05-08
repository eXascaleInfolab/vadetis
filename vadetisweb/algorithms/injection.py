import random
from vadetisweb.utils import stochastic_duration


def anomaly_injection(dataset, conf):

    df = dataset.dataframe
    df_class = dataset.dataframe_class

    df_inject = dataset.dataframe.copy()
    df_inject_class = dataset.dataframe_class.copy()
    time_series = dataset.timeseries_set.all()

    normal_lowerbound_duration = conf['normal_lowerbound_duration']
    normal_upperbound_duration = conf['normal_upperbound_duration']
    anomaly_lowerbound_duration = conf['anomaly_lowerbound_duration']
    anomaly_upperbound_duration = conf['anomaly_upperbound_duration']
    probability = conf['probability']

    for ts in time_series:
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
                for index, value in df.loc[df.index[anomaly_start_index:normal_start_index], ts.id].iteritems(): # df.iloc[anomaly_start_index:normal_start_index, df.columns.get_loc(ts.id)].iteritems():
                    # respect probability
                    if random.uniform(0, 1) <= probability:
                        # check if normal data at index -> change required
                        if df_class.loc[index, ts.id] == False:
                            inject_correlated_std_deviation_anomaly(df, df_inject, df_inject_class, index, ts.id)

    return df_inject, df_inject_class


#TODO change function
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
