from .rpca import *
from .rpca.baselines import *
from vadetisweb.parameters import F1_SCORE

def robust_pca(df, df_class, df_train, df_train_class, validated_data, maximize_score=F1_SCORE):

    # Transform it using Robust PCA
    huber_loss = loss.HuberLoss(delta=validated_data['delta'])
    rpca_transformer = MRobustPCA(2, huber_loss)
    X_rpca = rpca_transformer.fit_transform(df)

    X_rpca_inverse = rpca_transformer.inverse_transform(X_rpca)

    test1 = GreedyRPCA(X_rpca).fit_transform(df)
    test2 = GreedyRPCA(X_rpca).fit(df)

    return None
