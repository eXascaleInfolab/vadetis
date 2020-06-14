from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

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


# todo view in frontend for this class
class Location(models.Model):
    """
    The Location model holds the information about the location including label of a single time series.
    """

    label = models.CharField(max_length=32, null=False)
    lon = models.FloatField(null=False)
    lat = models.FloatField(null=False)
    ch1903_easting = models.PositiveIntegerField(null=True, blank=True)
    ch1903_northing = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return '%s' % (self.label)


class DataSet(models.Model):
    """
    The DataSet model holds all information about a dataset. A dataset is a collection of time series.
    """

    # human readable title for this dataset
    title = models.CharField(null=False, blank=False, max_length=128, help_text='Human readable title of the dataset')

    # owner of the dataset
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    # real world or synthetic
    type = models.CharField(null=False, max_length=32, choices=DATASET_TYPE, default=REAL_WORLD,
                            help_text='Determines whether this dataset is real world or synthetic data.')

    # flag if this set contains spatial time series
    spatial_data = models.CharField(null=False, max_length=32, choices=DATASET_SPATIAL_DATA, default=NON_SPATIAL,
                                    help_text='Determines whether this dataset is spatial or not. Spatial data requires geographic information about the time series recording location.')

    # pickled object field for the dataframe of values
    dataframe = PickledObjectField(null=True, compress=True)

    # pickled object field for the dataframe of classes (outlier / normal)
    dataframe_class = PickledObjectField(null=True, compress=True)

    # frequency of the data
    frequency = models.CharField(null=True, max_length=16,
                                 help_text='The frequency of the series in this dataset.')

    is_public = models.BooleanField(default=True, help_text='Determines if this dataset is public available.')

    # test data
    is_training_data = models.BooleanField(default=False)
    original_dataset = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='training_dataset')

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

        if self.is_training_data:
            if not self.original_dataset:
                raise ValueError('No original dataset specified for this test dataset!')
        else:
            if self.original_dataset:
                raise ValueError('An original dataset cannot be a test dataset!')

        super(DataSet, self).save(*args, **kwargs)

    def __str__(self):
        return '%s (%s)' % (self.title, self.id)


class TimeSeries(models.Model):
    """
    A time series for a singe feature that is part of a dataset.
    """

    name = models.CharField(max_length=32, null=False)
    datasets = models.ManyToManyField(
        DataSet)  # many to many because this series may refer to dataset and multiple training datasets as well
    # training_dataset = models.ForeignKey(TrainingDataset, null=True, on_delete=models.CASCADE)
    unit = models.CharField(max_length=32, choices=UNITS, null=False, help_text='Defines the unit of the values')
    is_spatial = models.BooleanField(default=False)
    location = models.OneToOneField(Location, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Time Series'

    def save(self, *args, **kwargs):
        """
        if self.dataset and self.training_dataset or not self.dataset and not self.training_dataset:
            raise ValueError('Exactly one of [TimeSeries.dataset, TimeSeries.training_dataset] must be set')
        """
        if self.is_spatial:
            if not self.location:
                raise ValueError('Spatial Time Series require a Location')

        super(TimeSeries, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.name)


@receiver(post_delete, sender=TimeSeries)
def auto_delete_location_with_ts(sender, instance, **kwargs):
    """
    In order to delete Location once a Time Series is deleted
    """
    instance.location.delete()
