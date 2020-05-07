from .rpca import *
from .rpca.baselines import *
from .helper_functions import df_anomaly_instances, get_train_valid_test_sets, estimate_score_bound

import pandas as pd

from vadetisweb.parameters import F1_SCORE

def robust_pca_huber_loss(df, df_class, df_train, df_train_class, delta=1, n_components=2, maximize_score=F1_SCORE, train_size=0.5, random_seed=10):

    df_train_class_instances = df_anomaly_instances(df_train_class)
    df_train = df_train.join(df_train_class_instances)

    df_class_instances = df_anomaly_instances(df_class)
    df_with_class_instances = df.join(df_class_instances)

    X_train, X_valid, X_test = get_train_valid_test_sets(df_train, train_size=train_size, random_seed=random_seed)

    # Dimensionality reduction with Robust PCA with Huber Loss Function
    huber_loss = loss.HuberLoss(delta=delta)
    rpca_transformer = MRobustPCA(n_components, huber_loss)

    # Train set
    X_train_reduced = rpca_transformer.fit_transform(X_train.drop('class', axis=1))
    X_train_reduced = pd.DataFrame(data=X_train_reduced, index=X_train_reduced.index)
    X_train_reconstructed = rpca_transformer.inverse_transform(X_train_reduced)
    X_train_reconstructed = pd.DataFrame(data=X_train_reconstructed, index=X_train_reconstructed.index)

    train_scores = normalized_anomaly_scores(X_train, X_train_reconstructed)

    # Valid set
    X_valid_reduced = rpca_transformer.fit_transform(X_valid.drop('class', axis=1))
    X_valid_reduced = pd.DataFrame(data=X_valid_reduced, index=X_valid_reduced.index)
    X_valid_reconstructed = rpca_transformer.inverse_transform(X_valid_reduced)
    X_valid_reconstructed = pd.DataFrame(data=X_valid_reconstructed, index=X_valid_reconstructed.index)

    valid_scores = normalized_anomaly_scores(X_valid, X_valid_reconstructed)

    higher = model.decision_function(valid[valid['class'] == False].drop('class', axis=1).values).mean()
    lower = model.decision_function(valid[valid['class'] == True].drop('class', axis=1).values).mean()

    lower_bound, higher_bound = estimate_score_bound(lower, higher) if lower <= higher else estimate_score_bound(higher, lower)
    thresholds = np.linspace(lower_bound, higher_bound, 100)



    return None


def normalized_anomaly_scores(df_original, df_reconstructed):
    """
    The reconstruction error is the sum of the squared differences between the original and the reconstructed dataset.
    The sum of the squared differences is scaled by the max-min range of the sum of the squared differences,
    so that all reconstruction errors are within a range of 0 to 1 (normalized).

    :param df_original: the original dataset as dataframe
    :param df_reconstructed: the reconstructed dataset from rpca
    :return: anomaly scores as series with range 0 to 1
    """

    diff = np.sum((np.array(df_original) - np.array(df_reconstructed)) ** 2, axis=1)
    diff = pd.Series(data=diff, index=df_original.index)
    diff = (diff - np.min(diff)) / (np.max(diff) - np.min(diff))

    return diff