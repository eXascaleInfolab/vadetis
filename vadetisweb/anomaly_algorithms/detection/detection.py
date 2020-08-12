from vadetisweb.parameters import TIME_RANGE_SELECTION
from vadetisweb.utils import get_detection_single_ts_results_json, get_common_detection_results_json, get_type_from_dataset_json
from .cluster import cluster_gaussian_mixture
from .helper_functions import df_range
from .histogram import histogram
from .isolation_forest import isolation_forest
from .lisa import lisa_pearson, lisa_dtw, lisa_geo
from .robust_pca import robust_pca_huber_loss
from .svm import svm


def lisa_pearson_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']
    window_size = validated_data['window_size']
    time_series_id = validated_data['time_series'].id

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'], start_offset=window_size)

    scores, y_hat_results, info, df_response, df_class_response = lisa_pearson(df, df_class, time_series_id, maximize_score=validated_data['maximize_score'], window_size=window_size)

    type = get_type_from_dataset_json(validated_data['dataset_series_json'])
    data_series = get_detection_single_ts_results_json(dataset, df_response, df_class_response, time_series_id, scores, y_hat_results, settings, type)

    return data_series, info


def lisa_dtw_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']
    window_size = validated_data['window_size']
    time_series_id = validated_data['time_series'].id

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'], start_offset=window_size)

    scores, y_hat_results, info, df_response, df_class_response = lisa_dtw(df, df_class, time_series_id, maximize_score=validated_data['maximize_score'], window_size=window_size, distance_function=validated_data['dtw_distance_function'])

    type = get_type_from_dataset_json(validated_data['dataset_series_json'])

    data_series = get_detection_single_ts_results_json(dataset, df_response, df_class_response, time_series_id, scores, y_hat_results, settings, type)

    return data_series, info


def lisa_geo_detection(df, df_class, validated_data, settings):
    dataset = validated_data['dataset']
    time_series_id = validated_data['time_series'].id

    if validated_data['time_range'] == TIME_RANGE_SELECTION:
        df, df_class = df_range(df, df_class, validated_data['range_start'], validated_data['range_end'])

    scores, y_hat_results, info = lisa_geo(df, df_class, time_series_id, maximize_score=validated_data['maximize_score'])

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
