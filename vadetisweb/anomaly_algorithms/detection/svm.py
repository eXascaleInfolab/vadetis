from sklearn.svm import OneClassSVM

from .helper_functions import *

from vadetisweb.utils import get_detection_meta

#########################################################
# SVM
#########################################################

def svm(df, df_class, df_train, df_train_class, maximize_score=F1_SCORE, gamma=0.000562, nu=0.5, kernel='rbf', train_size=0.5, random_seed=10):

    df_train_common_class = df_anomaly_instances(df_train_class)
    df_train_with_common_class = df_train.join(df_train_common_class)

    df_common_class = df_anomaly_instances(df_class)

    train, valid, test = get_train_valid_test_sets(df_train_with_common_class, train_size=train_size, random_seed=random_seed)

    model = OneClassSVM(gamma=gamma, nu=nu, kernel=kernel)
    model.fit(train.drop('class', axis=1).values)

    higher = model.decision_function(valid[valid['class'] == False].drop('class', axis=1).values).mean()
    lower = model.decision_function(valid[valid['class'] == True].drop('class', axis=1).values).mean()
    lower_bound, higher_bound = estimate_score_bound(lower, higher) if lower <= higher else estimate_score_bound(higher, lower)
    thresholds = np.linspace(lower_bound, higher_bound, 100)

    y_scores = model.decision_function(valid.drop('class', axis=1).values)
    training_threshold_scores = get_threshold_scores(thresholds, y_scores, valid['class'])
    selected_index = get_max_score_index_for_score_type(training_threshold_scores, maximize_score)
    selected_threshold = thresholds[selected_index]

    # detection on dataset
    scores = model.decision_function(df.values)
    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_common_class['class'].values.astype(int)
    detection_threshold_scores = get_threshold_scores(thresholds, scores, df_common_class['class'])
    info = get_detection_meta(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['training_threshold_scores'] = training_threshold_scores.tolist()
    info['detection_threshold_scores'] = detection_threshold_scores.tolist()

    return scores, y_hat_results, df_common_class, info
