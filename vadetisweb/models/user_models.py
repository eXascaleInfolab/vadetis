from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator, RegexValidator
from vadetisweb.models import TaskMixin


class UserTasks(TaskMixin, models.Model):
    # link UserTasks to a User model instance.
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'User Tasks'

    def __str__(self):
        return '%s' % (self.user.username)


class UserSettings(models.Model):
    """
    The User Profile contains User settings for the application.
    """

    # link UserProfile to a User model instance.
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    highcharts_height = models.PositiveIntegerField('Height of charts', null=False, default=500,
                                                    help_text='Value in pixels, Default: 500',
                                                    validators=[MinValueValidator(250)])
    legend_height = models.PositiveIntegerField('Height of chart legends', null=False, default=100,
                                                help_text='Value in pixels, Default: 100',
                                                validators=[MinValueValidator(50)])

    color_outliers = models.CharField('Color outliers', max_length=7, null=False, default="#FF0000",
                                      help_text='Default: #FF0000, the RGB color used to mark outliers',
                                      validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])

    color_clusters = models.CharField('Color for LISA clusters', max_length=7, null=False, default="#0000FF",
                                      help_text='Default: #0000FF, the RGB color used to mark LISA clusters of high or low values',
                                      validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])

    color_true_positive = models.CharField('Color for True Positives', max_length=7, null=False, default="#008800",
                                           help_text='Default: #008800, the RGB color used to mark true positives',
                                           validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])

    color_false_positive = models.CharField('Color for False Positives', max_length=7, null=False, default="#FF0000",
                                            help_text='Default: #FF0000, the RGB color used to mark false positives',
                                            validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])

    color_false_negative = models.CharField('Color for False Negatives', max_length=7, null=False, default="#0000FF",
                                            help_text='Default: #0000FF, the RGB color used to mark false negatives',
                                            validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])

    round_digits = models.PositiveIntegerField('Number of digits for results', null=False, default=3,
                                               help_text='Must be a number between 1 and 6',
                                               validators=[MinValueValidator(1), MaxValueValidator(6)])

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username
