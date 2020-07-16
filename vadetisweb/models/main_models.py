import numpy as np, pandas as pd
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

from model_utils.managers import InheritanceManager
from picklefield.fields import PickledObjectField
from pandas import DataFrame

from vadetisweb.parameters import *


#########################################################
# Vadetis Models
#########################################################

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    order = models.IntegerField(default=10, null=False, unique=False)

    def __str__(self):
        return '%s' % (self.name)


class FrequentlyAskedQuestion(models.Model):
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)

    question = models.CharField(max_length=255, null=False)
    answer = models.TextField(null=False, help_text="HTML allowed")

    def __str__(self):
        return '%s' % (self.question)


class Location(models.Model):
    """
    The Location model holds the information about the location including label of a single time series.
    """

    label = models.CharField(max_length=32, null=False)
    latitude = models.FloatField(null=False, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)])

    def __str__(self):
        return '%s' % (self.label)


class DataSet(models.Model):
    """
    The DataSet model holds all information about a dataset. A dataset is a collection of time series.
    """

    # human readable title for this dataset
    title = models.CharField(null=False, blank=False, max_length=64, help_text='Human readable title of the dataset')

    # owner of the dataset
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    # real world or synthetic
    type = models.CharField(null=False, max_length=32, choices=DATASET_TYPE, default=SYNTHETIC,
                            help_text='Determines whether this dataset is real-world or synthetic data.')

    # pickled object field for the dataframe of values
    dataframe = PickledObjectField(null=True, compress=True)

    # pickled object field for the dataframe of classes (outlier / normal)
    dataframe_class = PickledObjectField(null=True, compress=True)

    # frequency of the data
    granularity = models.CharField(null=True, max_length=16,
                                 help_text='The granularity of the series in this dataset.')

    shared = models.BooleanField(default=True, help_text='If shared, this dataset is visible to other users.')

    # test data
    training_data = models.BooleanField(default=False)
    main_dataset = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='training_dataset')

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Model Methods
    def number_of_dataframe_values(self):
        np_num_values = self.dataframe.count().sum()
        return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values

    def number_of_normal_values(self):
        df_class_count = self.dataframe_class.apply(pd.Series.value_counts).sum(axis=1)
        try:
            np_num_values = df_class_count.loc[False]
            return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values
        except KeyError:
            # if no False keys exists, this dataset does not have normal data
            return 0

    def number_of_anomaly_values(self):
        df_class_count = self.dataframe_class.apply(pd.Series.value_counts).sum(axis=1)
        try:
            np_num_values = df_class_count.loc[True]
            return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values
        except KeyError:
            # if no True keys exists, this dataset does not have anomalies
            return 0

    def contamination_level(self):
        return self.number_of_anomaly_values() / self.number_of_dataframe_values()

    def number_of_time_series_normal_values(self, ts_id):
        df_class_count = self.dataframe_class[ts_id].value_counts()
        try:
            np_num_values = df_class_count.loc[False]
            return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values
        except KeyError:
            # if no False keys exists, this series does not have anomalies
            return 0

    def number_of_time_series_anomaly_values(self, ts_id):
        df_class_count = self.dataframe_class[ts_id].value_counts()
        try:
            np_num_values = df_class_count.loc[True]
            return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values
        except KeyError:
            # if no True keys exists, this series does not have anomalies
            return 0

    def number_of_time_series_values(self, ts_id):
        np_num_values = self.dataframe[ts_id].count().sum()
        return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values

    def contamination_level_of_time_series(self, ts_id):
        return self.number_of_time_series_anomaly_values(ts_id) / self.number_of_time_series_values(ts_id)

    def number_of_training_datasets(self):
        return self.training_dataset.count()

    def number_of_shared_training_datasets(self):
        return self.training_dataset.filter(shared=True).count()

    def is_spatial(self):
        return all(ts.location is not None for ts in self.timeseries_set.all())

    class Meta:
        unique_together = ('title', 'owner',)

    def _check_dataframe(self):
        if not self.dataframe is None:
            if not (isinstance(self.dataframe, DataFrame)): raise ValueError(
                "Dataframe object is not a pandas dataframe")
        if not self.dataframe_class is None:
            if not (isinstance(self.dataframe, DataFrame)): raise ValueError(
                "Dataframe class object is not a pandas dataframe")

    def save(self, *args, **kwargs):
        # check dataframes are pandas dataframe objects
        self._check_dataframe()

        if self.training_data:
            if not self.main_dataset:
                raise ValueError('No original dataset specified for this training dataset!')
        else:
            if self.main_dataset:
                raise ValueError('An original dataset cannot be a training dataset!')

        super(DataSet, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.title)


class TimeSeries(models.Model):
    """
    A time series for a singe feature that is part of a dataset.
    """

    name = models.CharField(max_length=32, null=False)
    datasets = models.ManyToManyField(DataSet)  # many to many because this series may refer to dataset and multiple training datasets as well
    unit = models.CharField(max_length=32, choices=UNITS, null=False, help_text='Defines the unit of the values')
    location = models.OneToOneField(Location, null=True, on_delete=models.CASCADE)

    def is_spatial(self):
        return self.location is not None

    class Meta:
        verbose_name_plural = 'Time Series'

    def save(self, *args, **kwargs):
        super(TimeSeries, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.name)


@receiver(pre_delete, sender=DataSet)
def pre_delete_story(sender, instance, **kwargs):
    for ts in instance.timeseries_set.all():
        if ts.datasets.count() == 1:
            # ts is the only time series of this dataset that is going to be deleted, so delete it too
            ts.delete()

# @receiver(post_delete, sender=TimeSeries)
# def auto_delete_location_with_ts(sender, instance, **kwargs):
#     """
#     In order to delete Location once a Time Series is deleted
#     """
#     instance.location.delete()
