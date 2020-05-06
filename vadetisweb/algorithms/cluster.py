from sklearn.mixture import GaussianMixture

from vadetisweb.utils import get_info

from .helper_functions import *

#########################################################
# CLUSTER
#########################################################

def cluster_gaussian_mixture(df, df_class, df_train, df_train_class, maximize_score=F1_SCORE, n_components=3, n_init=3, train_size=0.5, random_seed=10):

    df_train_class_instances = df_anomaly_instances(df_train_class)
    df_train = df_train.join(df_train_class_instances)

    df_class_instances = df_anomaly_instances(df_class)
    df_with_class_instances = df.join(df_class_instances)

    train, valid, test = get_train_valid_test_sets(df_train, train_size=train_size, random_seed=random_seed)

    gmm = GaussianMixture(n_components=n_components, n_init=n_init, random_state=random_seed)
    gmm.fit(train.drop('class', axis=1).values)

    higher = gmm.score(valid[valid['class'] == False].drop('class', axis=1).values)
    lower = gmm.score(valid[valid['class'] == True].drop('class', axis=1).values)
    lower_bound, higher_bound = estimate_score_bound(lower, higher) if lower <= higher else estimate_score_bound(higher, lower)
    thresholds = np.linspace(lower_bound, higher_bound, 100)

    y_scores = gmm.score_samples(valid.drop('class', axis=1).values)
    threshold_scores = get_threshold_scores(thresholds, y_scores, valid)
    selected_index = get_max_score_index_for_score_type(threshold_scores, maximize_score)
    selected_threshold = thresholds[selected_index]

    scores = gmm.score_samples(df_with_class_instances.drop('class', axis=1).values)
    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_with_class_instances['class'].values.astype(int)
    info = get_info(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['threshold_scores'] = threshold_scores.tolist()

    return scores, y_hat_results, df_with_class_instances, info
