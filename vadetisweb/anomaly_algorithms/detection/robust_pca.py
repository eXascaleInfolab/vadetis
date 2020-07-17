from vadetisweb.utils import get_detection_meta

from .rpca import *
from .helper_functions import *


def robust_pca_huber_loss(df, df_class, df_train, df_train_class, delta=1, n_components=2, maximize_score=F1_SCORE, train_size=0.5, random_seed=10):

    df_train_common_class = df_anomaly_instances(df_train_class)
    df_common_class = df_anomaly_instances(df_class)

    # stratify parameter makes a split so that the proportion of values in the sample produced will be the same as the proportion of values provided to parameter stratify
    X_train, X_test, y_train, y_test = train_test_split(df_train, df_train_common_class, train_size=train_size, random_state=random_seed, stratify=df_train_common_class)

    # Dimensionality reduction with Robust PCA and Huber Loss Function
    huber_loss = loss.HuberLoss(delta=delta)
    M_rpca = MRobustPCA(n_components, huber_loss)

    # Fit R-PCA on Train Set
    M_rpca.fit(X_train)

    # R-PCA on Test Set
    X_test_reduced = M_rpca.transform(X_test)
    X_test_reduced = pd.DataFrame(data=X_test_reduced, index=X_test.index)
    X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
    X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed, index=X_test.index)

    y_test_scores = normalized_anomaly_scores(X_test, X_test_reconstructed)
    y_test_scores = np.round(y_test_scores, 7)  # round scores

    # computed scores are always in between 0-1 due to min max normalization
    thresholds = np.linspace(0, 1, 200)
    thresholds = np.round(thresholds, 7)  # round thresholds

    training_threshold_scores = get_threshold_scores(thresholds, y_test_scores, y_test, upper_boundary=True)
    selected_index = get_max_score_index_for_score_type(training_threshold_scores, maximize_score)
    selected_threshold = thresholds[selected_index]

    # Run on Dataset
    X_df_reduced = M_rpca.transform(df)
    X_df_reduced = pd.DataFrame(data=X_df_reduced, index=df.index)
    X_df_reconstructed = M_rpca.inverse_transform(X_df_reduced)
    X_df_reconstructed = pd.DataFrame(data=X_df_reconstructed, index=df.index)

    # detection on dataset
    scores = normalized_anomaly_scores(df, X_df_reconstructed)
    scores = np.round(scores, 7)  # round scores

    y_hat_results = (scores > selected_threshold).astype(int)
    y_truth = df_common_class.values.astype(int)
    detection_threshold_scores = get_threshold_scores(thresholds, scores, df_common_class['class'])
    info = get_detection_meta(selected_threshold, y_hat_results, y_truth, upper_boundary=True)

    info['thresholds'] = thresholds.tolist()
    info['training_threshold_scores'] = training_threshold_scores.tolist()
    info['detection_threshold_scores'] = detection_threshold_scores.tolist()

    return scores, y_hat_results, df_common_class, info


def normalized_anomaly_scores(df_original, df_reconstructed):
    """
    The reconstruction error is the sum of the squared differences between the original and the reconstructed dataset.
    The sum of the squared differences is scaled by the max-min range of the sum of the squared differences,
    so that all reconstruction errors are within a range of 0 to 1 (normalized). In consequence, normal data
    should have a low score whereas anomalies have higher scores.

    :param df_original: the original dataset as dataframe
    :param df_reconstructed: the reconstructed dataset from rpca
    :return: anomaly scores as series with range 0 to 1
    """

    diff = np.sum((np.array(df_original) - np.array(df_reconstructed)) ** 2, axis=1)
    diff = pd.Series(data=diff, index=df_original.index)
    diff = (diff - np.min(diff)) / (np.max(diff) - np.min(diff))

    return diff