from sklearn.ensemble import IsolationForest
from vadetisweb.utils import get_info
from .helper_functions import *

#########################################################
# ISOLATION FOREST
#########################################################

def isolation_forest(df, df_class, df_train, df_train_class, maximize_score=F1_SCORE, n_jobs=-1, bootstrap=True, n_estimators=40, train_size=0.5, random_seed=10):

    df_train_class_instances = df_anomaly_instances(df_train_class)
    df_train = df_train.join(df_train_class_instances)

    df_class_instances = df_anomaly_instances(df_class)
    df_with_class_instances = df.join(df_class_instances)

    train, valid, test = get_train_valid_test_sets(df_train, train_size=train_size, random_seed=random_seed)

    model = IsolationForest(random_state=random_seed, n_jobs=n_jobs, max_samples=train.shape[0], bootstrap=bootstrap, n_estimators=n_estimators)
    model.fit(train.drop('class', axis=1).values)

    higher = model.decision_function(valid[valid['class'] == False].drop('class', axis=1).values).mean()
    lower = model.decision_function(valid[valid['class'] == True].drop('class', axis=1).values).mean()
    lower_bound, higher_bound = estimate_score_bound(lower, higher) if lower <= higher else estimate_score_bound(higher, lower)
    thresholds = np.linspace(lower_bound, higher_bound, 100)

    y_scores = model.decision_function(valid.drop('class', axis=1).values)
    threshold_scores = get_threshold_scores(thresholds, y_scores, valid)
    selected_index = get_max_score_index_for_score_type(threshold_scores, maximize_score)
    selected_threshold = thresholds[selected_index]

    scores = model.decision_function(df_with_class_instances.drop('class', axis=1).values)
    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_with_class_instances['class'].values.astype(int)
    info = get_info(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['threshold_scores'] = threshold_scores.tolist()

    return scores, y_hat_results, df_with_class_instances, info
