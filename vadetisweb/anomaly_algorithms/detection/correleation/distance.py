import datetime
import logging
from math import hypot, sin, cos, sqrt, atan2, radians

import numpy as np
import pandas as pd

from vadetisweb.models import TimeSeries


def linear_distance(x1, y1, x2, y2):
    """
    Computes the 2-dim linear distance between to locations

    :param x1: location 1 x value
    :param y1: location 1 y value
    :param x2: location 2 x value
    :param y2: location 2 y value
    :return: the distance between two locations
    """

    distance = hypot(x2 - x1, y2 - y1)

    return distance


def three_dim_distance(distance_2d, h1, h2):
    """
    Computes the 3-dim linear distance between two locations

    :param distance_2d: the 2-dim distance between the two locations
    :param h1: location 1 height value
    :param h2: location 2 height value
    :return: the 3-dim distance
    """

    total_distance = hypot(distance_2d, h1 - h2)

    return total_distance


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Computes between to lat/lon locations using the haversine algorithm
    https://en.wikipedia.org/wiki/Haversine_formula

    :param lat1: location 1 latitude
    :param lon1: location 1 longitude
    :param lat2: location 2 latitude
    :param lon2: location 2 longitude
    :return: the distance between the two locations in KM
    """
    # radius of earth in km, approx.
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def get_df_corr_geo_distance(df):
    start_time = datetime.datetime.now()

    df_dist = df_distance(df)
    df_correlation = df_corr_geo_distance(df_dist)

    time_elapsed = (datetime.datetime.now() - start_time).__str__()
    logging.debug("Execution time for geographic correlation values: %s" % time_elapsed)

    return df_correlation


def df_distance(df):
    """
    Computes a geographical distance matrix where columns and row names represent station ids

    :param df: a dataframe of with columns as station names
    :return: a distance matrix as dataframe
    """

    df_dist = pd.DataFrame(index=df.columns, columns=df.columns)

    for ts_id_origin in df.columns:
        ts_origin = TimeSeries.objects.get(id=ts_id_origin)

        for ts_id_destination in df.columns:
            ts_destination = TimeSeries.objects.get(id=ts_id_destination)

            if ts_origin == ts_destination:
                distance = 0
            else:
                distance = haversine_distance(ts_origin.location.latitude,
                                              ts_origin.location.longitude,
                                              ts_destination.location.latitude,
                                              ts_destination.location.longitude)
            # set distance value
            df_dist.loc[ts_id_origin, ts_id_destination] = distance

    return df_dist


def df_corr_geo_distance(df):
    """
    Takes a distance matrix and returns inverse distance weighted matrix, so close distances are weighted more than
    those far away. Result is normalized (a row/col sums to 1).

    :param df: a pandas dataframe with distances between time series
    :return: a normalized inverse distance weighted matrix
    """
    df_corr = 1.0 / df.astype('float64') # to make ZeroDivision possible

    df_corr[np.isinf(df_corr)] = np.nan # inf -> NaN

    df_corr /= df_corr.sum(axis=0) # normalize, axis does not matter as symmetric matrix

    return df_corr
