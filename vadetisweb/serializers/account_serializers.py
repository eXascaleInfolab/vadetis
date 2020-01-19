from rest_framework import serializers
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator, RegexValidator
from vadetisweb.models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    The form for the settings of the user
    """

    highcharts_height = serializers.IntegerField(default=500,
                                                 help_text='Value in pixels, Default: 500',
                                                 validators=[MinValueValidator(250)],
                                                 style={'template': 'vadetisweb/parts/input/text_input.html'})

    legend_height = serializers.IntegerField(default=100,
                                             help_text='Value in pixels, Default: 100',
                                             validators=[MinValueValidator(50)],
                                             style={'template': 'vadetisweb/parts/input/text_input.html'})

    color_outliers = serializers.CharField(max_length=7, default="#FF0000",
                                           help_text='Default: #FF0000, the RGB color used to mark outliers',
                                           validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                  'input_class': 'minicolors-input'})

    color_clusters = serializers.CharField(max_length=7, default="#0000FF",
                                           help_text='Default: #0000FF, the RGB color used to mark LISA clusters of high or low values',
                                           validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                  'input_class': 'minicolors-input'})

    color_true_positive = serializers.CharField(max_length=7, default="#008800",
                                                help_text='Default: #008800, the RGB color used to mark true positives',
                                                validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                                style={'template': 'vadetisweb/parts/input/text_input.html',
                                                       'input_class': 'minicolors-input'})

    color_false_positive = serializers.CharField(max_length=7, default="#FF0000",
                                                 help_text='Default: #FF0000, the RGB color used to mark false positives',
                                                 validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                                 style={'template': 'vadetisweb/parts/input/text_input.html',
                                                        'input_class': 'minicolors-input'})

    color_false_negative = serializers.CharField(max_length=7, default="#0000FF",
                                                 help_text='Default: #0000FF, the RGB color used to mark false negatives',
                                                 validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                                 style={'template': 'vadetisweb/parts/input/text_input.html',
                                                        'input_class': 'minicolors-input'})

    round_digits = serializers.IntegerField(default=3,
                                            help_text='Must be a number between 1 and 6',
                                            validators=[MinValueValidator(1), MaxValueValidator(6)],
                                            style={'template': 'vadetisweb/parts/input/text_input.html',
                                                   'class': 'form-group-last'})

    class Meta:
        model = UserSettings
        fields = ('highcharts_height', 'legend_height', 'color_outliers', 'color_clusters',
                  'color_true_positive', 'color_false_positive', 'color_false_negative', 'round_digits')
