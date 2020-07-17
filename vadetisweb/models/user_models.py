from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from vadetisweb.parameters import *


class UserSetting(models.Model):
    """
    The user settings for the application.
    """

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

    def __str__(self):
        if self.user is not None:
            return self.user.username
        else:
            return 'Settings'
