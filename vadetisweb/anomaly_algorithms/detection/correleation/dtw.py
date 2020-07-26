import numpy as np
from scipy.spatial.distance import cdist

import pyximport; pyximport.install()
from .cutil import cutil
#import vadetisweb.anomaly_algorithms.detection.correleation.cutil.cutil as cutil

#########################################################
# DTW
#########################################################

def dtw(x, y, distance):
    """
    Computes Dynamic Time Warping (DTW) of two sequences. It uses the cdist function from scipy
    (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html)
    Some code taken from https://github.com/pierre-rouanet/dtw

    :param x: N1*M array
    :param y: N2*M array
    :param string or func distance: distance parameter for cdist. When string is given, cdist uses optimized functions
    for the distance metrics. If a string is passed, the distance function can be
    'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean', 'hamming',
    'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
    'sokalmichener', 'sokalsneath', 'sqeuclidean', 'wminkowski', 'yule'.

    :return: minimum distance, the cost matrix, the accumulated cost matrix, and the wrap path
    """
    assert( len(x)>0 )
    assert( len(y)>0 )

    if np.ndim(x) == 1:
        x = x.reshape(-1,1) #reshapes array ex.: array([2, 4, 0, 1 ]) -> array([[2],[4],[0],[1]]), needed for cdist

    if np.ndim(y) == 1:
        y = y.reshape(-1,1)

    len_x, len_y = len(x), len(y)

    D0 = np.zeros((len_x + 1, len_y + 1))
    D0[0, 1:] = np.inf
    D0[1:, 0] = np.inf

    D1 = D0[1:, 1:] #reference to inner view of D0
    D0[1:,1:] = cdist(x, y, distance)

    #CM = D1.copy() #the cost matrix
    #print(CM)

    """
    for i in range(len_x):
        for j in range(len_y):
            D1[i, j] += min(D0[i, j], D0[i, j + 1], D0[i + 1, j])
    """

    cutil.min_cumsum(D0) # cythonized version of cost accumulation

    #print(D0)

    if len_x == 1:
        path = np.zeros(len_y, dtype=np.int8), np.array(range(len_y))
    elif len_y == 1:
        path = np.array(range(len_x)), np.zeros(len_x, dtype=np.int8)
    else:
        #i, j = np.array(D0.shape) - 2
        #path = cutil._traceback(D0, i, j) #_pathfinder(D0)
        path = _pathfinder(D0)

    #dist, cost, acc, path
    #return D1[-1, -1] / sum(D1.shape), CM, D1, path

    # only need path
    return path


def _pathfinder(DM):
    i, j = np.array(DM.shape) - 2
    p, q = [i], [j]

    while ((i > 0) or (j > 0)):
        tb = np.argmin((DM[i, j], DM[i, j+1], DM[i+1, j]))
        if (tb == 0):
            i -= 1
            j -= 1
        elif (tb == 1):
            i -= 1
        else: # (tb == 2):
            j -= 1
        p.insert(0, i) #cast to int
        q.insert(0, j) #cast to int

    return np.array(p, dtype=int), np.array(q, dtype=int)