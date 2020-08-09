
#########################################################
# Anomaly Detection Algorithms
#########################################################

LISA_PEARSON = 'LISA (Pearson)'
LISA_DTW_PEARSON = 'LISA (DTW with Pearson)'
LISA_SPATIAL = 'LISA (Spatial)'
RPCA_HUBER_LOSS = 'RPCA (Huber Loss Function)'
HISTOGRAM = 'Histogram'
CLUSTER_GAUSSIAN_MIXTURE = 'Cluster (Gaussian Mixture)'
SVM = 'SVM'
ISOLATION_FOREST = 'Isolation Forest'

ANOMALY_DETECTION_ALGORITHMS = (
    (LISA_PEARSON, LISA_PEARSON),
    (LISA_DTW_PEARSON, LISA_DTW_PEARSON),
    (LISA_SPATIAL, LISA_SPATIAL),
    (RPCA_HUBER_LOSS, RPCA_HUBER_LOSS),
    (HISTOGRAM, HISTOGRAM),
    (CLUSTER_GAUSSIAN_MIXTURE, CLUSTER_GAUSSIAN_MIXTURE),
    (SVM, SVM),
    (ISOLATION_FOREST, ISOLATION_FOREST),
)

ANOMALY_DETECTION_ALGORITHMS_NON_SPATIAL = (
    (LISA_PEARSON, LISA_PEARSON),
    (LISA_DTW_PEARSON, LISA_DTW_PEARSON),
    (RPCA_HUBER_LOSS, RPCA_HUBER_LOSS),
    (HISTOGRAM, HISTOGRAM),
    (CLUSTER_GAUSSIAN_MIXTURE, CLUSTER_GAUSSIAN_MIXTURE),
    (SVM, SVM),
    (ISOLATION_FOREST, ISOLATION_FOREST),
)

ANOMALY_DETECTION_ALGORITHMS_NON_SPATIAL_NON_TRAINING = (
    (LISA_PEARSON, LISA_PEARSON),
    (LISA_DTW_PEARSON, LISA_DTW_PEARSON),
)

ANOMALY_DETECTION_ALGORITHMS_NON_TRAINING = (
    (LISA_PEARSON, LISA_PEARSON),
    (LISA_DTW_PEARSON, LISA_DTW_PEARSON),
    (LISA_SPATIAL, LISA_SPATIAL),
)

#########################################################
# Anomaly Detection Score Types
#########################################################

F1_SCORE = 'F1-Score'
PRECISION = 'Precision'
RECALL = 'Recall'
ACCURACY = 'Accuracy'
NMI = 'Normalized Mutual Information'
RMSE = 'Root Mean Square Error'

ANOMALY_DETECTION_SCORE_TYPES = (
    (F1_SCORE, F1_SCORE),
    (PRECISION, PRECISION),
    (RECALL, RECALL),
    (ACCURACY, ACCURACY),
    (NMI, NMI),
    (RMSE, RMSE),
)

#########################################################
# Anomaly Types
#########################################################

ANOMALY_TYPE_POINT = 'Point outlier(s)'
ANOMALY_TYPE_AMPLITUDE_SHIFT = 'Amplitude Shift'
ANOMALY_TYPE_GROWTH_CHANGE = 'Growth Change'
ANOMALY_TYPE_DISTORTION = 'Distortion'
ANOMALY_TYPE_MISSING_VALUES = 'Missing Values'

ANOMALY_INJECTION_TYPES = (
    (ANOMALY_TYPE_POINT, ANOMALY_TYPE_POINT),
    (ANOMALY_TYPE_AMPLITUDE_SHIFT, ANOMALY_TYPE_AMPLITUDE_SHIFT),
    (ANOMALY_TYPE_GROWTH_CHANGE, ANOMALY_TYPE_GROWTH_CHANGE),
    (ANOMALY_TYPE_DISTORTION, ANOMALY_TYPE_DISTORTION),
    (ANOMALY_TYPE_MISSING_VALUES, ANOMALY_TYPE_MISSING_VALUES),
)

ANOMALY_INJECTION_SCALE_SMALL = 'Small'
ANOMALY_INJECTION_SCALE_MEDIUM = 'Medium'
ANOMALY_INJECTION_SCALE_HIGH = 'High'
ANOMALY_INJECTION_SCALE_RANDOM = 'Random'

ANOMALY_INJECTION_SCALE = (
    (ANOMALY_INJECTION_SCALE_SMALL, ANOMALY_INJECTION_SCALE_SMALL),
    (ANOMALY_INJECTION_SCALE_MEDIUM, ANOMALY_INJECTION_SCALE_MEDIUM),
    (ANOMALY_INJECTION_SCALE_HIGH, ANOMALY_INJECTION_SCALE_HIGH),
    (ANOMALY_INJECTION_SCALE_RANDOM, ANOMALY_INJECTION_SCALE_RANDOM),
)

ANOMALY_INJECTION_REPEAT_SINGLE = 'Single'
ANOMALY_INJECTION_REPEAT_INTERVAL_LOW = 'Repeat (Low Frequency)'
ANOMALY_INJECTION_REPEAT_INTERVAL_MEDIUM = 'Repeat (Medium Frequency)'
ANOMALY_INJECTION_REPEAT_INTERVAL_HIGH = 'Repeat (High Frequency)'

ANOMALY_INJECTION_REPETITIONS = (
    (ANOMALY_INJECTION_REPEAT_SINGLE, ANOMALY_INJECTION_REPEAT_SINGLE),
    (ANOMALY_INJECTION_REPEAT_INTERVAL_LOW, ANOMALY_INJECTION_REPEAT_INTERVAL_LOW),
    (ANOMALY_INJECTION_REPEAT_INTERVAL_MEDIUM, ANOMALY_INJECTION_REPEAT_INTERVAL_MEDIUM),
    (ANOMALY_INJECTION_REPEAT_INTERVAL_HIGH, ANOMALY_INJECTION_REPEAT_INTERVAL_HIGH),
)

#########################################################
# Supported SVM Kernels
#########################################################

KERNEL_RBF = 'rbf'
KERNEL_LINEAR = 'linear'
KERNEL_POLY = 'poly'
KERNEL_SIGMOID = 'sigmoid'

SVM_KERNELS = (
    (KERNEL_RBF, KERNEL_RBF),
    (KERNEL_LINEAR, KERNEL_LINEAR),
    (KERNEL_POLY, KERNEL_POLY),
    (KERNEL_SIGMOID, KERNEL_SIGMOID),
)

#########################################################
# Units for the datasets
#########################################################

VALUE = 'Value'
QUANTITY = 'Quantity'
BOOLEAN = 'Boolean'
KG = 'Kilogram'
G = 'Gram'
AMPERE = 'Ampere'
VOLT = 'Volt'
JOULE = 'Joule'
CELSIUS = 'Celsius'
KELVIN = 'Kelvin'
KMH = 'KM/H'
MS = 'M/S'
HPA = 'hPa'
KNOTS = 'Knots'
LUX = 'Lux'
MILLIMETER = 'Millimeter'
MILLIMETER_PER_DAY = 'Millimeter per day'
MILLIVOLT = 'Millivolt'
MILLIWATT_PER_M2 = 'Milliwatt per m2'
HOURS = 'Hours'
OCTAS = 'Octas'
PERCENT = 'Percent'
DEGREE = 'Degree'
VOLT = 'Volt'
WATTS_PER_M2 = 'Watts per m2'
CENTIMETERS = 'Centimeters'

UNITS = (
    (VALUE, VALUE),
    (QUANTITY, QUANTITY),
    (BOOLEAN, BOOLEAN),
    (KG, KG),
    (G, G),
    (CELSIUS, CELSIUS),
    (KELVIN, KELVIN),
    (KMH, KMH),
    (MS, MS),
    (HPA, HPA),
    (KNOTS, KNOTS),
    (LUX, LUX),
    (MILLIMETER, MILLIMETER),
    (MILLIMETER_PER_DAY, MILLIMETER_PER_DAY),
    (AMPERE, AMPERE),
    (VOLT, VOLT),
    (JOULE, JOULE),
    (MILLIVOLT, MILLIVOLT),
    (MILLIWATT_PER_M2, MILLIWATT_PER_M2),
    (HOURS, HOURS),
    (OCTAS, OCTAS),
    (PERCENT, PERCENT),
    (DEGREE, DEGREE),
    (VOLT, VOLT),
    (WATTS_PER_M2, WATTS_PER_M2),
    (CENTIMETERS, CENTIMETERS),
)

#########################################################
#Types of datasets
#########################################################

SYNTHETIC = 'Synthetic'
REAL_WORLD = 'Real World'

DATASET_TYPE = (
    (SYNTHETIC, SYNTHETIC),
    (REAL_WORLD, REAL_WORLD),
)

NON_SPATIAL = 'Non Spatial'
SPATIAL = 'Spatial'

DATASET_SPATIAL_DATA  = (
    (NON_SPATIAL, NON_SPATIAL),
    (SPATIAL, SPATIAL),
)

#########################################################
# Correlation Algorithms
#########################################################

TIME_RANGE_SELECTION = 'Selection'
TIME_RANGE_FULL = 'Full Range'

TIME_RANGE = (
    (TIME_RANGE_SELECTION, TIME_RANGE_SELECTION),
    (TIME_RANGE_FULL, TIME_RANGE_FULL),
)

EUCLIDEAN = "euclidean"
BRAYCURTIS = "braycurtis"
CANBERRA = "canberra"
CHEBYSHEV = "chebyshev"
CITYBLOCK = "cityblock"
CORRELATION = "correlation"
COSINE = "cosine"
DICE = "dice"
HAMMING = "hamming"
JACCARD = "jaccard"
KULSINSKI = "kulsinski"
MAHALANOBIS = "mahalanobis"
MATCHING = "matching"
MINKOWSKI = "minkowski"
ROGERSTANIMOTO = "rogerstanimoto"
RUSSELLRAO = "russellrao"
SEUCLIDEAN = "seuclidean"
SOKALMICHENER = "sokalmichener"
SOKALSNEATH = "sokalsneath"
SQEUCLIDEAN = "sqeuclidean"
WMINKOWSKI = "wminkowski"
YULE = "yule"

DTW_DISTANCE_FUNCTION = (
    (EUCLIDEAN, EUCLIDEAN),
    (BRAYCURTIS, BRAYCURTIS),
    (CANBERRA, CANBERRA),
    (CHEBYSHEV, CHEBYSHEV),
    (CITYBLOCK, CITYBLOCK),
    (CORRELATION, CORRELATION),
    (COSINE, COSINE),
    (DICE, DICE),
    (HAMMING, HAMMING),
    (JACCARD, JACCARD),
    (KULSINSKI, KULSINSKI),
    (MAHALANOBIS, MAHALANOBIS),
    (MATCHING, MATCHING),
    (MINKOWSKI, MINKOWSKI),
    (ROGERSTANIMOTO, ROGERSTANIMOTO),
    (RUSSELLRAO, RUSSELLRAO),
    (SEUCLIDEAN, SEUCLIDEAN),
    (SOKALMICHENER, SOKALMICHENER),
    (SOKALSNEATH, SOKALSNEATH),
    (SQEUCLIDEAN, SQEUCLIDEAN),
    (WMINKOWSKI, WMINKOWSKI),
    (YULE, YULE),
)

#########################################################
# Defaults for application settings
#########################################################

DEFAULT_COLOR_OUTLIERS = '#C30000'
DEFAULT_COLOR_TRUE_POSITIVES = '#008800'
DEFAULT_COLOR_FALSE_POSITIVES = '#FF0000'
DEFAULT_COLOR_FALSE_NEGATIVES = '#0000FF'

DEFAULT_SETTINGS = (
    ('color_outliers', DEFAULT_COLOR_OUTLIERS),
    ('color_true_positive', DEFAULT_COLOR_TRUE_POSITIVES),
    ('color_false_positive', DEFAULT_COLOR_FALSE_POSITIVES),
    ('color_false_negative', DEFAULT_COLOR_FALSE_NEGATIVES),
)

#########################################################
# Misc
#########################################################

BOOLEAN_SELECTION = (
    ('', ''),
    ('true', 'true'),
    ('false', 'false'),
)
