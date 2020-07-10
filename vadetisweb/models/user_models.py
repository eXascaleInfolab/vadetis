from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator, RegexValidator

from vadetisweb.models import TaskMixin
from vadetisweb.parameters import *


class UserTasks(TaskMixin, models.Model):
    # link UserTasks to a User model instance.
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'User Tasks'

    def __str__(self):
        return '%s' % (self.user.username)


class UserSetting(models.Model):
    """
    The User Profile contains User settings for the application.
    """

    # link UserProfile to a User model instance.
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    color_outliers = models.CharField('Color outliers', max_length=7, null=False, default=DEFAULT_COLOR_OUTLIERS,
                                      help_text='Default: #C30000, the RGB color used to mark outliers',
                                      validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])

    color_true_positive = models.CharField('Color for True Positives', max_length=7, null=False, default=DEFAULT_COLOR_TRUE_POSITIVES,
                                           help_text='Default: #008800, the RGB color used to mark true positives',
                                           validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])

    color_false_positive = models.CharField('Color for False Positives', max_length=7, null=False, default=DEFAULT_COLOR_FALSE_POSITIVES,
                                            help_text='Default: #FF0000, the RGB color used to mark false positives',
                                            validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])

    color_false_negative = models.CharField('Color for False Negatives', max_length=7, null=False, default=DEFAULT_COLOR_FALSE_NEGATIVES,
                                            help_text='Default: #0000FF, the RGB color used to mark false negatives',
                                            validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')])

    round_digits = models.PositiveIntegerField('Round digits', null=False, default=DEFAULT_ROUND_DIGITS,
                                               help_text='Used to set the decimal places for the presentation. Must be a number between 1 and 6',
                                               validators=[MinValueValidator(1), MaxValueValidator(6)])

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username
