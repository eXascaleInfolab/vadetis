import numpy as np, pandas as pd
import datetime, logging

from .dtw import dtw

from vadetisweb.utils import next_earlier_dt

#########################################################
# PEARSON HELPER FUNCTIONS
#########################################################

def _sum_of_squares(values):
    """
    Squares each value of a list of values and returns the sum of it

    :param values: a list of values
    :return: the sum of squared values
    """
    return sum(n ** 2 for n in values)


def _sequences_from_path(x, y, path):
    #print("x:", x)
    #print("path_x:", path[0])
    x_dtw = x[path[0]]
    #print("y:", y)
    #print("path_y:", path[1])
    y_dtw = y[path[1]]

    return x_dtw, y_dtw

#########################################################
# PEARSON
#########################################################

def pearson_matrix(df, min_periods=None):
    """
    Returns a symmetric matrix of Pearson correlation values using all values to calculate the correlation

    :param df: the dataframe
    :param min_periods: the minimum number of values needed calculate a single correlation, otherwise result is NaN
    :return: a symmetric matrix of Pearson correlation values
    """
    start_time = datetime.datetime.now()
    df_pm = df.corr(method='pearson', min_periods=min_periods)
    time_elapsed = (datetime.datetime.now() - start_time).__str__()
    logging.debug("Execution time for pearson matrix:", time_elapsed)
    return df_pm


def pearson(df, time_series_id, window_size=2, min_periods=None, absolute_values=True):
    """
    Calculates the Pearson correlation between a series and a dataframe column-wise using a rolling window

    :param df: a dataframe
    :param time_series_id: the id of the station to calculate the correlations for
    :param window_size: The size of the moving window
    :param min_periods: the minimum number of values needed calculate a single correlation, otherwise result is NaN
    :return: the correlation dataframe
    """
    assert (window_size >= 2)

    start_time = datetime.datetime.now()

    series = df[time_series_id]
    df_corr = df.rolling(window=window_size, min_periods=min_periods).corr(series)

    # sometimes -inf or inf values are in correlation dataframe, because of same values during window length where Pearson is undef.
    # replace them with nan
    df_corr = df_corr.replace([np.inf, -np.inf], np.nan)

    # to make row standardization possible
    del df_corr[time_series_id]

    time_elapsed = (datetime.datetime.now() - start_time).__str__()
    logging.debug("Execution time for pearson values for series:", time_elapsed)

    if absolute_values:
        return df_corr.abs(), time_elapsed

    return df_corr, time_elapsed


def most_correlated(df, station_id, num=3):
    """
    For a given station ID, it finds the most n correlated time series using Pearson correlation.

    :param df: a dataframe
    :param station_id: the station ID one wants the find the most n correlated time series, must be a colums in the dataframe
    :param num: the number of most correlated time series in the result
    :return: dict of the most correlated time series (id and value)
    """
    df_pearson = pearson_matrix(df)
    sorted_pearson = df_pearson.drop(station_id)[station_id].sort_values(ascending=False)
    most_n_correlated = sorted_pearson.iloc[1:num + 1].index.values #exclude first value at index 0

    return most_n_correlated


def pearson_corr_coeff(X, Y):
    """
    Calculates the Pearson correlation between two given 1-dim arrays of values

    :param X: a array of values
    :param Y: a array of values
    :return: the Pearson correlation coefficient
    """
    assert(len(X) == len(Y))

    #if all x_i and/or y_i are equal, Pearson is undef.
    if (np.unique(X).size == 1) or (np.unique(Y).size == 1):
        return np.nan

    #print("X:", X)
    #print("Y:", Y)

    x_mean = X.mean()
    y_mean = Y.mean()

    #print("X-Mean: ", x_mean)
    #print("Y-Mean: ", y_mean)

    XM = [x - x_mean for x in X]
    YM = [y - y_mean for y in Y]

    #print("XM:", XM)
    #print("YM:", YM)

    r_numerator = sum(np.asarray(XM) * np.asarray(YM)) #add.reduce() is equivalent to sum()
    r_denominator = np.sqrt(_sum_of_squares(XM)) * np.sqrt(_sum_of_squares(YM))

    #print("r_numerator:", r_numerator)
    #print("r_denominator:", r_denominator)

    try:
        weight = r_numerator / r_denominator
    except ZeroDivisionError:
        pass
        print("Division by Zero occurred")
        weight = np.nan

    #print("weight:", weight)
    return weight


def dtw_pearson(df, time_series_id, distance, window_size=2, absolute_values=True):
    """
    Computes the Pearson correlation using DTW for a given station id to all other time series of the same dataset.
    The DTW path defines the mapping of the values.

    :param df: time indexed dataframe containing all time series values
    :param time_series_id: the ID of the time series to calculate the Pearson correlation for
    :param string or func distance: distance parameter for cdist, see method dtw()
    :param window_size: the size of the moving window
    :return: a dataframe containing the DTW with Pearson correlation values
    """
    assert (window_size >= 2)

    past_size = window_size - 1 #a window of 2 means only one past value, later needed in _next_dt

    start_time = datetime.datetime.now()

    # empty correlation dataframe
    df_corr = pd.DataFrame(index=df.index, columns=df.columns)

    # to make row standardization possible
    # df_corr.loc[:,time_series_id] = 0 #set to 0
    del df_corr[time_series_id]

    # get time series ids before adding column for mean and lisa
    time_series_ids = df_corr.columns.tolist()

    index_dts = list(df_corr.index.values)

    # iterate over all time frames
    for index_dt in index_dts:
        win_end_index_dt = pd.to_datetime(index_dt)
        win_start_index_dt = next_earlier_dt(win_end_index_dt, df.index.inferred_freq, past_size)

        df_part = df.loc[win_start_index_dt: win_end_index_dt]

        if df_part.shape[0] == window_size: #window must be of size

            x = df_part[time_series_id].dropna().values

            # check if x is empty (as all entries are NaN)
            if len(x) == 0:
                continue

            for ts_id in time_series_ids:

                y = df_part[ts_id].dropna().values

                # check if y is empty (as all entries are NaN)
                if len(y) == 0:
                    continue

                path = dtw(x, y, distance=distance)

                x_dtw, y_dtw = _sequences_from_path(x, y, path)

                weight = pearson_corr_coeff(x_dtw, y_dtw)

                if absolute_values:
                    weight = np.absolute(weight)

                #df_corr.loc[win_end_index_dt, station] = weight #faster
                df_corr.at[win_end_index_dt, ts_id] = weight

    time_elapsed = (datetime.datetime.now() - start_time).__str__()

    logging.debug("Execution time for pearson values using dtw:", time_elapsed)
    return df_corr, time_elapsed
