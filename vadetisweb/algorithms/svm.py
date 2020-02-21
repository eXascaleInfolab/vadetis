from sklearn.svm import OneClassSVM

from vadetisweb.utils import get_info

from .helper_functions import *

#########################################################
# SVM
#########################################################

def svm(df, df_class, df_train, df_train_class, maximize_score=F1_SCORE, gamma=0.000562, nu=0.5, kernel='rbf', train_size=0.5, random_seed=42):

    df_train_class_instances = df_anomaly_instances(df_train_class)
    df_train = df_train.join(df_train_class_instances)

    df_class_instances = df_anomaly_instances(df_class)
    df_with_class_instances = df.join(df_class_instances)

    train, valid, test = get_train_valid_test_sets(df_train, train_size=train_size, random_seed=random_seed)

    model = OneClassSVM(gamma=gamma, nu=nu, kernel=kernel)
    model.fit(train.drop('Class', axis=1).values)

    higher = model.decision_function(valid[valid['Class'] == False].drop('Class', axis=1).values).mean()
    lower = model.decision_function(valid[valid['Class'] == True].drop('Class', axis=1).values).mean()
    lower_bound, higher_bound = estimate_score_bound(lower, higher) if lower <= higher else estimate_score_bound(higher, lower)
    thresholds = np.linspace(lower_bound, higher_bound, 100)

    y_scores = model.decision_function(valid.drop('Class', axis=1).values)
    threshold_scores = get_threshold_scores(thresholds, y_scores, valid)
    selected_index = get_max_score_index_for_score_type(threshold_scores, maximize_score)
    selected_threshold = thresholds[selected_index]

    scores = model.decision_function(df_with_class_instances.drop('Class', axis=1).values)
    scores = scores.flatten() #bug, its corrected in next version of scikit-learn

    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_with_class_instances['Class'].values.astype(int)
    info = get_info(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['threshold_scores'] = threshold_scores.tolist()

    return scores, y_hat_results, df_with_class_instances, info
