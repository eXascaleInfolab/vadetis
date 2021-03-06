
from vadetisweb.models import DataSet


def dataset_not_found_msg(dataset_id):
    return 'Dataset "' + str(dataset_id) + '" was not found'


def dataset_saved_msg(dataset_id):
    try:
        dataset = DataSet.objects.get(id=dataset_id)
        return 'Dataset "%s" saved' % dataset.title

    except DataSet.DoesNotExist:
        raise ValueError("Dataset with id %s does not exist" % dataset_id)


def dataset_removed_msg(dataset_title):
    return 'Dataset "%s" removed' % dataset_title


def msg_injection_all_anomalies():
    return "Cannot compute an anomaly in a range that contains only anomalies"


def dataset_imported_msg(title):
    return "Dataset '%s' has been imported. Now, you can add training data." % title


def training_dataset_imported_msg(title):
    return "Training Dataset '%s' has been imported" % title