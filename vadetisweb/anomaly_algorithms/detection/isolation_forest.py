from sklearn.ensemble import IsolationForest
from .helper_functions import *
from vadetisweb.utils import get_detection_meta, min_max_normalization

#########################################################
# ISOLATION FOREST
#########################################################

def isolation_forest(df, df_class, df_train, df_train_class, maximize_score=F1_SCORE, n_jobs=-1, bootstrap=True, n_estimators=40, train_size=0.5, random_seed=10):

    df_train_common_class = df_anomaly_instances(df_train_class)
    df_train_with_common_class = df_train.join(df_train_common_class)

    df_common_class = df_anomaly_instances(df_class)

    train, valid, test = get_train_valid_test_sets(df_train_with_common_class, train_size=train_size, random_seed=random_seed)

    model = IsolationForest(random_state=random_seed, n_jobs=n_jobs, max_samples=train.shape[0], bootstrap=bootstrap, n_estimators=n_estimators)
    model.fit(train.drop('class', axis=1).values)

    thresholds = np.linspace(0, 1, 200)

    y_scores = min_max_normalization(model.decision_function(valid.drop('class', axis=1).values))
    training_threshold_scores = get_threshold_scores(thresholds, y_scores, valid['class'])
    selected_index = get_max_score_index_for_score_type(training_threshold_scores, maximize_score)
    selected_threshold = thresholds[selected_index]

    # detection on dataset
    scores = min_max_normalization(model.decision_function(df.values))
    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_common_class['class'].values.astype(int)
    detection_threshold_scores = get_threshold_scores(thresholds, scores, df_common_class['class'])
    info = get_detection_meta(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['training_threshold_scores'] = training_threshold_scores.tolist()
    info['detection_threshold_scores'] = detection_threshold_scores.tolist()

    return scores, y_hat_results, df_common_class, info
