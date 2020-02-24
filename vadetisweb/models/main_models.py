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
class Station(models.Model):
    """
    The Station model holds the information including identifier, label and location of a single spatial entity that
    recorded various time series.
    """

    label = models.CharField(max_length=32, null=False)
    lon = models.FloatField(null=False)
    lat = models.FloatField(null=False)
    ch1903_easting = models.PositiveIntegerField(null=True)
    ch1903_northing = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)

    def __str__(self):
        return '%s' % (self.label)


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


class CorrelationSetting(models.Model):
    """
    The CorrelationSetting model holds the information about the correlation setting of an applied LISA calculation
    """

    # type of correlation algorithm
    algorithm = models.CharField(null=False, max_length=32, choices=CORRELATION_ALGORITHMS)

    # allows to filter for subclasses
    # see: https://django-model-utils.readthedocs.io/en/latest/managers.html#inheritancemanager
    objects = InheritanceManager()


class Pearson(CorrelationSetting):
    """
    Inherits from Correlation Setting and holds the parameters for a Pearson calculation including moving window size
    and min periods.
    """

    window_size = models.PositiveIntegerField(null=False)
    min_periods = models.PositiveIntegerField(null=True)
    row_standardized = models.BooleanField(null=False)

    class Meta:
        unique_together = ('window_size', 'min_periods', 'row_standardized',)

    def dropdown_str(self):
        return '%s, W: %s, Min P: %s, Std: %s' % (
        self.algorithm, self.window_size, self.min_periods, self.row_standardized)

    def __str__(self):
        return '%s - Window Size: %s, Min Periods: %s, Row-Std.: %s' % (
        self.algorithm, self.window_size, self.min_periods, self.row_standardized)


class GeoDistance(CorrelationSetting):
    """
    Inherits from Correlation Setting and holds the distance function used for a geographical distance calculation.
    """

    distance_function = models.CharField(null=False, max_length=64, choices=GEO_DISTANCE)

    class Meta:
        unique_together = ('distance_function',)

    def dropdown_str(self):
        return '%s, F: %s' % (self.algorithm, self.distance_function)

    def __str__(self):
        return '%s - Distance Func: %s' % (self.algorithm, self.distance_function)


class DTWPearson(CorrelationSetting):
    """
    Inherits from Correlation Setting and holds the parameters for a DTW with Pearson calculation including moving
    window size and distance function.
    """

    window_size = models.PositiveIntegerField(null=False)
    distance_function = models.CharField(null=False, max_length=64, choices=DTW_DISTANCE_FUNCTION)
    row_standardized = models.BooleanField(null=False)

    class Meta:
        unique_together = ('window_size', 'distance_function', 'row_standardized',)

    def dropdown_str(self):
        return '%s, W: %s, Func: %s, Std: %s' % (
        self.algorithm, self.window_size, self.distance_function, self.row_standardized)

    def __str__(self):
        return '%s - Window Size: %s, Distance Func: %s, Row-Std.: %s' % (
        self.algorithm, self.window_size, self.distance_function, self.row_standardized)


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


class PreprocessedData(models.Model):
    """
    The PreprocessedData model refers to preprocessed anomaly detection results.
    """

    # type of correlation algorithm
    algorithm = models.CharField(null=False, max_length=32, choices=ANOMALY_DETECTION_ALGORITHMS)
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE, null=False, related_name="preprocessed_data")

    # owner of the preprocessed data
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    execution_time = models.DurationField(null=False)

    # allows to filter for subclasses
    # see: https://django-model-utils.readthedocs.io/en/latest/managers.html#inheritancemanager
    objects = InheritanceManager()

    def __str__(self):
        return '%s - %s' % (self.algorithm, self.dataset)


class PreprocessedLISA(PreprocessedData):
    """
    Inherits from PreprocessedData and holds the parameters for a LISA computation.
    """

    # correlation settings performed on this preprocessed data
    correlation_setting = models.ForeignKey(CorrelationSetting, on_delete=models.CASCADE, null=False)

    def __str__(self):
        setting = CorrelationSetting.objects.filter(id=self.correlation_setting.id).get_subclass()

        if isinstance(setting, Pearson):
            return '%s - Window Size: %s, Min Periods: %s, Row-Std.: %s' % (setting.algorithm,
                                                                            setting.window_size,
                                                                            setting.min_periods,
                                                                            setting.row_standardized)

        elif isinstance(setting, DTWPearson):
            return '%s - Window Size: %s, Distance Func: %s, Row-Std.: %s' % (
                setting.algorithm, setting.window_size, setting.distance_function, setting.row_standardized)
        else:
            return '%s - Distance Func: %s' % (setting.algorithm, setting.distance_function)


class LisaComputation(models.Model):
    """
    The LISA computation model contains all information about a LISA computation for one time series including the
    LISA scores and correlation that was used.
    """

    # the preprocessed data this computation belongs to
    preprocessed_data = models.ForeignKey(PreprocessedLISA, on_delete=models.CASCADE, null=True,
                                          related_name="lisa_computation")

    # the station that corresponds to this correlation values
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=False, related_name="lisa_computation")

    # pickled object field for the lisa values as pandas dataframe
    dataframe_lisa = PickledObjectField(null=False, compress=True)

    # pickled object field for the correlation values as pandas dataframe
    dataframe_correlation = PickledObjectField(null=False, compress=True)

    class Meta:
        unique_together = ('station', 'preprocessed_data',)

    def _check_frames(self):
        if not (isinstance(self.dataframe_lisa, DataFrame)): raise Exception(
            "Dataframe lisa variable is not a pandas dataframe")
        if not (isinstance(self.dataframe_correlation, DataFrame)): raise Exception(
            "Dataframe correlation variable is not a pandas dataframe")

    def _settings_to_dropdown_str(self):
        """
        Ugly hack to get the subclass of the settings
        :return: string representation of settings subclass
        """
        subclass_setting = CorrelationSetting.objects.get_subclass(id=self.correlation_setting.id)
        return subclass_setting.dropdown_str()

    def _settings_to_str(self):
        """
        Ugly hack to get the subclass of the settings
        :return: string representation of settings subclass
        """
        subclass_setting = CorrelationSetting.objects.get_subclass(id=self.correlation_setting.id)
        return subclass_setting.__str__()

    def save(self, *args, **kwargs):
        # check if a dataframe was saved
        self._check_frames()
        super(LisaComputation, self).save(*args, **kwargs)

    def dropdown_str(self):
        settings_str = self._settings_to_dropdown_str()

        return '%s' % (settings_str)

    def __str__(self):
        settings_str = self._settings_to_str()

        return '%s - %s' % (self.station.name, settings_str)
