from .lisa import lisa_pearson, lisa_dtw, lisa_geo
from .histogram import histogram
from .cluster import cluster_gaussian_mixture
from .svm import svm
from .isolation_forest import isolation_forest
from .robust_pca import robust_pca_huber_loss
from .helper_functions import df_range

from vadetisweb.utils import get_detection_single_ts_results_json, get_common_detection_results_json, get_type_from_dataset_json
from vadetisweb.parameters import TIME_RANGE_SELECTION


def lisa_pearson_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']
    window_size = validated_data['window_size']
    time_series_id = validated_data['time_series'].id

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'], start_offset=window_size)

    scores, y_hat_results, info = lisa_pearson(df, df_class, validated_data)

    # leave out the first x values (window size-1) from the beginning of the datasets as we cannot compute LISA for these values
    offset = window_size - 1
    scores = scores[offset:]
    y_hat_results = y_hat_results[offset:]
    df_response = df.iloc[offset:]
    df_class_response = df_class.iloc[offset:]

    type = get_type_from_dataset_json(validated_data['dataset_series_json'])
    data_series = get_detection_single_ts_results_json(dataset, df_response, df_class_response, time_series_id, scores, y_hat_results, settings, type)

    return data_series, info


def lisa_dtw_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']
    window_size = validated_data['window_size']
    time_series_id = validated_data['time_series'].id

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'], start_offset=window_size)

    scores, y_hat_results, info = lisa_dtw(df, df_class, validated_data)

    # leave out the first x values (window size-1) from the beginning of the datasets as we cannot compute LISA for these values
    offset = window_size - 1
    scores = scores[offset:]
    y_hat_results = y_hat_results[offset:]
    df_response = df.iloc[offset:]
    df_class_response = df_class.iloc[offset:]

    type = get_type_from_dataset_json(validated_data['dataset_series_json'])

    data_series = get_detection_single_ts_results_json(dataset, df_response, df_class_response, time_series_id, scores, y_hat_results, settings, type)

    return data_series, info


def lisa_geo_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']
    time_series_id = validated_data['time_series'].id

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'])

    scores, y_hat_results, info = lisa_geo(df, df_class, validated_data)

    type = get_type_from_dataset_json(validated_data['dataset_series_json'])

    data_series = get_detection_single_ts_results_json(dataset, df, df_class, time_series_id, scores, y_hat_results, settings, type)

    return data_series, info


def rpca_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']

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
    type = get_type_from_dataset_json(validated_data['dataset_series_json'])
    data_series = get_common_detection_results_json(dataset, df, df_class, df_common_class, scores, y_hat_results, settings, type)
    return data_series, info


def histogram_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']
    training_dataset = validated_data['training_dataset']
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'])

    scores, y_hat_results, df_common_class, info = histogram(df, df_class, df_train, df_train_class,
                                                             maximize_score=validated_data['maximize_score'],
                                                             train_size=validated_data['train_size'])
    type = get_type_from_dataset_json(validated_data['dataset_series_json'])
    data_series = get_common_detection_results_json(dataset, df, df_class, df_common_class, scores, y_hat_results, settings, type)
    return data_series, info


def cluster_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']

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
    type = get_type_from_dataset_json(validated_data['dataset_series_json'])
    data_series = get_common_detection_results_json(dataset, df, df_class, df_common_class, scores, y_hat_results, settings, type)
    return data_series, info


def svm_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']

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
    type = get_type_from_dataset_json(validated_data['dataset_series_json'])
    data_series = get_common_detection_results_json(dataset, df, df_class, df_common_class, scores, y_hat_results, settings, type)
    return data_series, info


def isolation_forest_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']

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

    type = get_type_from_dataset_json(validated_data['dataset_series_json'])
    data_series = get_common_detection_results_json(dataset, df, df_class, df_common_class, scores, y_hat_results, settings, type)
    return data_series, info
