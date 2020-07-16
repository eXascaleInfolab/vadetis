
from ..detection import *

from vadetisweb.parameters import TIME_RANGE_SELECTION


def lisa_pearson_recommendation(df, df_class, validated_data):
    window_size = validated_data['window_size']

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'], start_offset=window_size)

    scores, y_hat_results, info = lisa_pearson(df, df_class, validated_data)

    return info


def lisa_dtw_recommendation(df, df_class, validated_data):
    window_size = validated_data['window_size']
    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'], start_offset=window_size)

    scores, y_hat_results, info = lisa_dtw(df, df_class, validated_data)

    return info


def lisa_geo_recommendation(df, df_class, validated_data):
    scores, y_hat_results, info = lisa_geo(df, df_class, validated_data)

    return info


def rpca_recommendation(df, df_class, validated_data, ):

    training_dataset = validated_data['training_dataset']
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'])

    scores, y_hat_results, df_common_class, info = robust_pca_huber_loss(df, df_class, df_train, df_train_class,
                                                                         delta=validated_data['delta'],
                                                                         n_components=validated_data['n_components'],
                                                                         maximize_score=validated_data['maximize_score'],
                                                                         train_size=validated_data['train_size'])

    return info


def histogram_recommendation(df, df_class, validated_data):
    training_dataset = validated_data['training_dataset']
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'])

    scores, y_hat_results, df_common_class, info = histogram(df, df_class, df_train, df_train_class,
                                                             maximize_score=validated_data['maximize_score'],
                                                             train_size=validated_data['train_size'])

    return info


def cluster_recommendation(df, df_class, validated_data):
    training_dataset = validated_data['training_dataset']
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'])

    scores, y_hat_results, df_common_class, info = cluster_gaussian_mixture(df, df_class, df_train, df_train_class,
                                                                            maximize_score=validated_data['maximize_score'],
                                                                            n_components=validated_data['n_components'],
                                                                            n_init=validated_data['n_init'],
                                                                            train_size=validated_data['train_size'])

    return info


def svm_recommendation(df, df_class, validated_data):
    training_dataset = validated_data['training_dataset']
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'])

    scores, y_hat_results, df_common_class, info = svm(df, df_class, df_train, df_train_class,
                                                       maximize_score=validated_data['maximize_score'],
                                                       gamma=validated_data['gamma'],
                                                       nu=validated_data['nu'],
                                                       kernel=validated_data['kernel'],
                                                       train_size=validated_data['train_size'])
    return info


def isolation_forest_recommendation(df, df_class, validated_data):
    training_dataset = validated_data['training_dataset']
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'])

    scores, y_hat_results, df_common_class, info = isolation_forest(df, df_class, df_train,
                                                                    df_train_class,
                                                                    maximize_score=validated_data['maximize_score'],
                                                                    n_jobs=-1,
                                                                    bootstrap=validated_data['bootstrap'],
                                                                    n_estimators=validated_data['n_estimators'],
                                                                    train_size=validated_data['train_size'])

    return info