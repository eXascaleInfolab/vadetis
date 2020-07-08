import datetime

from .helper_functions import *
from .correleation.pearson import pearson, dtw_pearson
from .correleation.distance import get_df_corr_geo_distance

from vadetisweb.utils import df_zscore, get_detection_meta
#########################################################
# LISA HELPER
#########################################################

def z_pi(v_xi, v_i_mean, std_deviation_i):
    """
    Calculates the z value for time series p at a time i

    :param v_xi: the value of time series p at time i
    :param v_i_mean: the mean value at time i over all time series
    :param std_deviation_i: the standard deviation at time i
    :return: the z value
    """

    try:
        z_pi = (v_xi - v_i_mean) / std_deviation_i
    except ZeroDivisionError:
        print("Division by Zero occurred")
        z_pi = np.nan

    return z_pi


def lisa_for_df_row(df_part, time_series_id_p, time_series_ids, df_corr_part, skipna=True,
                    output_intermediate_results=False, output_intermediate_results_round=3):
    """
    Calculates a single LISA value

    :param df_part: the dataframe at time i, should be a single row resp. a single datetime index
    :param time_series_id_p: the time series id to calculate the lisa values for; refers to p parameter
    :param time_series_ids: the time series ids of the dataframe
    :param df_corr_part: the datafram that holds the correlation values
    :param skipna: determines if the algorithm excludes NaN values; a mathematical operation with NaN results in NaN otherwise
    :return: a LISA value
    """
    # np.seterr(all='raise', divide='raise', over='raise', under='raise', invalid='raise')

    # v_pi
    v_pi = df_part[time_series_id_p]
    # print("v_pi:\t", v_pi)

    # mean
    v_i_mean = df_part['mean']
    # print("v_i_mean:\t", v_i_mean)

    # std deviation, axis over columns as we calculate over singe row
    # ddof = 0: population standard deviation using n; ddof = 1: sample std deviation using n-1
    std_deviation_i = df_part.loc[time_series_ids].std(skipna=skipna, level=None, ddof=0)
    # print("std_deviation_i:\t", std_deviation_i)

    z_pi_val = z_pi(v_pi, v_i_mean, std_deviation_i)
    # print("z_pi_val:\t", z_pi_val)

    w_z_results = []
    w_z_items = []

    station_ids_iter = list(time_series_ids)
    station_ids_iter.remove(time_series_id_p)

    for station_id in station_ids_iter:
        v_qi = df_part[station_id]
        w_pq = df_corr_part[station_id]

        z_qi = z_pi(v_qi, v_i_mean, std_deviation_i)
        w_z_result = w_pq * z_qi
        w_z_results.append(w_z_result)

        if output_intermediate_results:
            w_z_item = {station_id: {'v_qi': round(v_qi, output_intermediate_results_round),
                                     'w_pq': round(w_pq, output_intermediate_results_round),
                                     'z_qi': round(z_qi, output_intermediate_results_round),
                                     'w_z_result': round(w_z_result, output_intermediate_results_round)}}
            w_z_items.append(w_z_item)

    # print("w_z_results:\t", w_z_results)

    if skipna:
        if np.isnan(w_z_results).all():  # If all values of w_z_results are np.NaN, LISA values should also be np.NaN
            w_z_results_sum = np.NaN
            lisa_value = np.NaN
        else:
            w_z_results_sum = np.nansum(w_z_results)
            lisa_value = z_pi_val * w_z_results_sum
    else:
        w_z_results_sum = sum(w_z_results)
        lisa_value = z_pi_val * sum(w_z_results)

    if output_intermediate_results:
        return lisa_value, v_pi, v_i_mean, std_deviation_i, z_pi_val, w_z_items, w_z_results_sum

    return lisa_value


def df_lisa_time_series(time_series_id_p, df_mean, df_corr, global_correlation=False, skipna=True):
    """
    Calculates the LISA values for a given time series id

    :param time_series_id_p: the time series id to calculate the lisa values for; refers to p parameter
    :param df_mean: the dataframe with all values of the time series, must have a column with the mean values of each row
    :param df_corr: the correlation dataframe to use for the calculation
    :param global_correlation: determines if the correlation dataframe is global or time indexed
    :return: the dataframe (as series) holding all LISA values for station id p
    """
    # np.seterr(all='raise', divide='raise', over='raise', under='raise', invalid='raise')

    start_time = datetime.datetime.now()

    # empty results dataframe
    df_results = pd.DataFrame(index=df_mean.index)
    # pre-populate results values for time series
    df_results[time_series_id_p] = np.nan  # numpy NaN

    # check if mean values already present, later used in lisa_for_df_row
    if 'mean' not in df_mean.columns:
        df_mean = df_copy_with_mean(df_mean)

    # get time series ids
    time_series_ids = df_mean.columns.drop('mean').tolist()

    # all datetime indexes
    index_dts = list(df_mean.index)

    for index_dt in index_dts:
        # converted_index_dt = pd.to_datetime(index_dt)
        # converted_index_dt = index_dt

        if global_correlation:
            df_results.loc[index_dt, time_series_id_p] = lisa_for_df_row(df_mean.loc[index_dt],
                                                                      time_series_id_p,
                                                                      time_series_ids, df_corr.loc[time_series_id_p],
                                                                      skipna=skipna)
        else:
            df_results.loc[index_dt, time_series_id_p] = lisa_for_df_row(df_mean.loc[index_dt],
                                                                      time_series_id_p,
                                                                      time_series_ids, df_corr.loc[index_dt],
                                                                      skipna=skipna)

    time_elapsed = (datetime.datetime.now() - start_time).__str__()
    print("Execution time for lisa values:", time_elapsed)

    return df_results


#########################################################
# PEARSON
#########################################################

def lisa_pearson(df, df_class, validated_data):

    window_size = validated_data['window_size']
    time_series = validated_data['time_series']
    row_standardized = validated_data['row_standardized']

    # mean values of each row of dataframe
    df_mean = df_copy_with_mean(df)

    df_class_copy = df_class.copy()
    df_class_copy = df_class_copy.rename(columns={time_series.id: 'class'})
    df_with_class_instances = df.join(df_class_copy['class'])

    df_correlation, correlation_time_elapsed = pearson(df, time_series.id, window_size=window_size)

    # apply row standardization if needed
    if row_standardized:
        df_correlation = df_row_standardized(df_correlation)

    # LISA Time Series
    df_results = df_lisa_time_series(time_series.id, df_mean, df_correlation)

    # get highest and lowest lisa values
    lower = df_results.min()[time_series.id]
    higher = df_results.max()[time_series.id]
    thresholds = np.linspace(lower, higher, 100)

    threshold_scores = get_threshold_scores(thresholds, df_results[time_series.id].values, df_with_class_instances)
    selected_index = get_max_score_index_for_score_type(threshold_scores, F1_SCORE)
    selected_threshold = thresholds[selected_index]

    scores = df_results[time_series.id].values
    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_class_copy['class'].values.astype(int)
    info = get_detection_meta(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['detection_threshold_scores'] = threshold_scores.tolist()

    return scores, y_hat_results, df_with_class_instances, info


#########################################################
# DTW
#########################################################

def lisa_dtw(df, df_class, validated_data):

    window_size = validated_data['window_size']
    time_series = validated_data['time_series']
    row_standardized = validated_data['row_standardized']
    distance_function = validated_data['dtw_distance_function']

    # mean values of each row of dataframe
    df_mean = df_copy_with_mean(df)

    df_class_copy = df_class.copy()
    df_class_copy = df_class_copy.rename(columns={time_series.id: 'class'})
    df_with_class_instances = df.join(df_class_copy['class'])

    df_correlation, correlation_time_elapsed = dtw_pearson(df, time_series.id, distance_function, window_size=window_size)

    # apply row standardization if needed
    if row_standardized:
        df_correlation = df_row_standardized(df_correlation)

    # LISA Time Series
    df_results = df_lisa_time_series(time_series.id, df_mean, df_correlation)

    # get highest and lowest lisa values
    lower = df_results.min()[time_series.id]
    higher = df_results.max()[time_series.id]
    thresholds = np.linspace(lower, higher, 100)

    threshold_scores = get_threshold_scores(thresholds, df_results[time_series.id].values, df_with_class_instances)
    selected_index = get_max_score_index_for_score_type(threshold_scores, F1_SCORE)
    selected_threshold = thresholds[selected_index]

    scores = df_results[time_series.id].values
    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_class_copy['class'].values.astype(int)
    info = get_detection_meta(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['detection_threshold_scores'] = threshold_scores.tolist()

    return scores, y_hat_results, df_with_class_instances, info



#########################################################
# GEO Distance
#########################################################

def lisa_geo(df, df_class, conf, time_series_id):
    df_corr_dist, _ = get_df_corr_geo_distance(df)

    df_class_copy = df_class.copy()
    df_class_copy = df_class_copy.rename(columns={time_series_id: 'class'})
    df_with_class_instances = df.join(df_class_copy['class'])

    # append mean values of each row to dataframe
    df_val_mean = df_copy_with_mean(df)

    print(df_corr_dist)

    # LISA Time Series
    df_lisa_results, lisa_time_elapsed = df_lisa_time_series(time_series_id, df_val_mean, df_corr_dist, global_correlation=True)

    # get highest and lowest lisa values
    higher = df_lisa_results.max()[time_series_id]
    lower = df_lisa_results.min()[time_series_id]
    thresholds = np.linspace(lower, higher, 100)

    threshold_scores = get_threshold_scores(thresholds, df_lisa_results.values, df_with_class_instances)
    selected_index = get_max_score_index_for_score_type(threshold_scores, F1_SCORE)
    selected_threshold = thresholds[selected_index]

    scores = df_lisa_results.values
    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_class_copy['class'].values.astype(int)
    info = get_detection_meta(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['training_threshold_scores'] = threshold_scores.tolist()

    return scores, y_hat_results, df_with_class_instances, info
