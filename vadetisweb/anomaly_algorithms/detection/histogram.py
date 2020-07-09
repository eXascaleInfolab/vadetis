from .helper_functions import *

from vadetisweb.utils import get_detection_meta

#########################################################
# HISTOGRAM
#########################################################

class hist_model(object):

    def __init__(self, bins=50):
        self.bins = bins

    def fit(self, X):

        bin_height, bin_edge = [], []

        for var in X.T:
            # get bins height and interval
            bh, bedge = np.histogram(var, bins=self.bins, density=True)
            bin_height.append(bh)
            bin_edge.append(bedge)

        self.bin_height = np.array(bin_height)
        self.bin_edge = np.array(bin_edge)

    def predict(self, X):
        scores = []
        for obs in X:
            obs_scores = []
            for i, var in enumerate(obs):
                # find which bin observation is in
                bin_num = (var > self.bin_edge[i]).argmin() - 1
                obs_scores.append(self.bin_height[i, bin_num])  # find bin height
            scores.append(np.mean(obs_scores))

        return np.array(scores)


def histogram(df, df_class, df_train, df_train_class, maximize_score=F1_SCORE, train_size=0.5, random_seed=10):

    df_train_common_class = df_anomaly_instances(df_train_class)
    df_train_with_common_class = df_train.join(df_train_common_class)

    df_common_class = df_anomaly_instances(df_class)

    train, valid, test = get_train_valid_test_sets(df_train_with_common_class, train_size=train_size, random_seed=random_seed)

    # square root of number of instances as number of bins
    num_bins = (np.sqrt(train.shape[0])).astype(int)
    logging.debug('Number of bins %d' % num_bins)

    # create and train model
    model = hist_model(bins=num_bins)
    model.fit(train.drop('class', axis=1).values)

    # get the scores for normality and abnormality in the validation set
    higher = np.median(model.predict(valid[valid['class'] == False].drop('class', axis=1).values))
    lower = np.median(model.predict(valid[valid['class'] == True].drop('class', axis=1).values))
    lower_bound, higher_bound = estimate_score_bound(lower, higher) if lower <= higher else estimate_score_bound(higher, lower)

    thresholds = np.linspace(lower_bound, higher_bound, 100)
    y_scores = model.predict(valid.drop('class', axis=1).values)
    training_threshold_scores = get_threshold_scores(thresholds, y_scores, valid['class'])
    selected_index = get_max_score_index_for_score_type(training_threshold_scores, maximize_score)
    selected_threshold = thresholds[selected_index]

    # detection on dataset
    scores = model.predict(df.values)
    y_hat_results = (scores < selected_threshold).astype(int)
    y_truth = df_common_class['class'].values.astype(int)
    detection_threshold_scores = get_threshold_scores(thresholds, scores, df_common_class['class'])
    info = get_detection_meta(selected_threshold, y_hat_results, y_truth)

    info['thresholds'] = thresholds.tolist()
    info['training_threshold_scores'] = training_threshold_scores.tolist()
    info['detection_threshold_scores'] = detection_threshold_scores.tolist()

    return scores, y_hat_results, df_common_class, info
