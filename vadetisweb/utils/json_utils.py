import numpy as np
from django.urls import reverse
from vadetisweb.parameters import REAL_WORLD

def datatable_dataset_rows(data, datasets):

    for dataset in datasets:
        row = []

        if dataset.type == REAL_WORLD:
            link = reverse('vadetisweb:dataset_real_world', args=[dataset.id])
        else:
            link = reverse('vadetisweb:dataset_synthetic', args=[dataset.id])

        np_num_values = dataset.dataframe.count().sum()

        dataset_link = '<a href="%s">%s (%s)</a>' % (link, dataset.title, dataset.id)
        row.append(dataset_link)
        row.append(dataset.owner.username)
        row.append(dataset.timeseries_set.count())
        row.append(int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values) # numpy int32/64 is not json serializable
        row.append(dataset.frequency)
        row.append(dataset.type_of_data)
        row.append(dataset.spatial_data)
        row.append(dataset.training_dataset.count())

        data.append(row)

    return data