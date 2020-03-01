from vadetisweb.utils import get_anomaly_detection_single_ts_results_json, get_anomaly_detection_ts_results_json

from .lisa import lisa_pearson, lisa_dtw, lisa_geo
from .histogram import histogram
from .cluster import cluster_gaussian_mixture
from .svm import svm
from .isolation_forest import isolation_forest


def perform_lisa_person(df, df_class, conf, ts_selected_id, dataset, settings):
    scores, y_hat_results, df_with_class_instances, info = lisa_pearson(df, df_class, conf, ts_selected_id)
    data_series = get_anomaly_detection_single_ts_results_json(dataset, ts_selected_id,
                                                               df_with_class_instances, scores, y_hat_results,
                                                               settings)
    return data_series, info


def perform_lisa_dtw(df, df_class, conf, ts_selected_id, dataset, settings):
    scores, y_hat_results, df_with_class_instances, info = lisa_dtw(df, df_class, conf, ts_selected_id)
    data_series = get_anomaly_detection_single_ts_results_json(dataset, ts_selected_id,
                                                               df_with_class_instances, scores, y_hat_results,
                                                               settings)
    return data_series, info


def perform_lisa_geo(df, df_class, conf, ts_selected_id, dataset, settings):
    scores, y_hat_results, df_with_class_instances, info = lisa_geo(df, df_class, conf,
                                                                    ts_selected_id)
    data_series = get_anomaly_detection_single_ts_results_json(dataset, ts_selected_id,
                                                               df_with_class_instances, scores,
                                                               y_hat_results, settings)
    return data_series, info


def perform_histogram(df, df_class, conf, training_dataset, dataset, settings):
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    scores, y_hat_results, df_with_class_instances, info = histogram(df, df_class, df_train, df_train_class,
                                                                     maximize_score=conf['maximize_score'],
                                                                     train_size=conf['train_size'],
                                                                     random_seed=conf['random_seed'])

    data_series = get_anomaly_detection_ts_results_json(dataset, df_with_class_instances, scores, y_hat_results,
                                                        settings)
    return data_series, info


def perform_cluster(df, df_class, conf, training_dataset, dataset, settings):
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    scores, y_hat_results, df_with_class_instances, info = cluster_gaussian_mixture(df, df_class, df_train,
                                                                                    df_train_class,
                                                                                    maximize_score=conf[
                                                                                        'maximize_score'],
                                                                                    n_components=conf[
                                                                                        'n_components'],
                                                                                    n_init=conf['n_init'],
                                                                                    train_size=conf[
                                                                                        'train_size'],
                                                                                    random_seed=conf[
                                                                                        'random_seed'])
    data_series = get_anomaly_detection_ts_results_json(dataset, df_with_class_instances, scores, y_hat_results,
                                                        settings)
    return data_series, info


def perform_svm(df, df_class, conf, training_dataset, dataset, settings):
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    scores, y_hat_results, df_with_class_instances, info = svm(df, df_class, df_train, df_train_class,
                                                               maximize_score=conf['maximize_score'],
                                                               gamma=conf['gamma'],
                                                               nu=conf['nu'],
                                                               kernel=conf['kernel'],
                                                               train_size=conf['train_size'],
                                                               random_seed=conf['random_seed'])
    data_series = get_anomaly_detection_ts_results_json(dataset, df_with_class_instances, scores, y_hat_results,
                                                        settings)
    return data_series, info


def perform_isolation_forest(df, df_class, conf, training_dataset, dataset, settings):
    df_train = training_dataset.dataframe
    df_train_class = training_dataset.dataframe_class

    scores, y_hat_results, df_with_class_instances, info = isolation_forest(df, df_class, df_train,
                                                                            df_train_class,
                                                                            maximize_score=conf[
                                                                                'maximize_score'],
                                                                            n_jobs=-1,
                                                                            bootstrap=conf['bootstrap'],
                                                                            n_estimators=conf[
                                                                                'n_estimators'],
                                                                            train_size=conf['train_size'],
                                                                            random_seed=conf['random_seed'])

    data_series = get_anomaly_detection_ts_results_json(dataset, df_with_class_instances, scores, y_hat_results,
                                                        settings)
    return data_series, info
