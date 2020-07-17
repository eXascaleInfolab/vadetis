from sklearn.svm import OneClassSVM

from .helper_functions import *

from vadetisweb.utils import get_detection_meta, min_max_normalization

#########################################################
# SVM
#########################################################

def svm(df, df_class, df_train, df_train_class, maximize_score=F1_SCORE, gamma=0.000562, nu=0.5, kernel='rbf', train_size=0.5, random_seed=10):

    df_train_common_class = df_anomaly_instances(df_train_class)
    df_train_with_common_class = df_train.join(df_train_common_class)

    df_common_class = df_anomaly_instances(df_class)

    train, valid = get_train_valid_sets(df_train_with_common_class, train_size=train_size, random_seed=random_seed)

    model = OneClassSVM(gamma=gamma, nu=nu, kernel=kernel)
    model.fit(train.drop('class', axis=1).values)

    thresholds = np.linspace(0, 1, 200)
    thresholds = np.round(thresholds, 7)  # round thresholds

    y_scores = min_max_normalization(model.decision_function(valid.drop('class', axis=1).values))
    y_scores = np.round(y_scores, 7)  # round scores

    training_threshold_scores = get_threshold_scores(thresholds, y_scores, valid['class'])
    selected_index = get_max_score_index_for_score_type(training_threshold_scores, maximize_score)
    selected_threshold = thresholds[selected_index]

    # detection on dataset
    scores = min_max_normalization(model.decision_function(df.values))
    scores = np.round(scores, 7)  # round scores

    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_common_class['class'].values.astype(int)
    detection_threshold_scores = get_threshold_scores(thresholds, scores, df_common_class['class'])
    info = get_detection_meta(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['training_threshold_scores'] = training_threshold_scores.tolist()
    info['detection_threshold_scores'] = detection_threshold_scores.tolist()

    return scores, y_hat_results, df_common_class, info
