from rest_framework import serializers
from allauth.account import app_settings
from allauth.account.forms import get_adapter as get_account_adapter, filter_users_by_email
from allauth.socialaccount.models import SocialAccount
from allauth.utils import get_username_max_length

from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator, RegexValidator

from vadetisweb.models import UserSetting, User
from vadetisweb.validators import username_validators, email_validators, alphabetic_validator
from vadetisweb.fields import RoundDigitsField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserSettingSerializer(serializers.ModelSerializer):
    """
    The form for the settings of the user
    """

    round_digits = RoundDigitsField(default=3, min_value=1, max_value=6,
                                    validators=[MinValueValidator(1), MaxValueValidator(6)], )

    color_outliers = serializers.CharField(max_length=7, default="#C30000",
                                           help_text='Default: #C30000, the RGB color used to mark outliers',
                                           validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                  'input_type': 'color'})

    color_true_positive = serializers.CharField(max_length=7, default="#008800",
                                                help_text='Default: #008800, the RGB color used to mark true positives',
                                                validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                                style={'template': 'vadetisweb/parts/input/text_input.html',
                                                       'input_type': 'color'})

    color_false_positive = serializers.CharField(max_length=7, default="#FF0000",
                                                 help_text='Default: #FF0000, the RGB color used to mark false positives',
                                                 validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                                 style={'template': 'vadetisweb/parts/input/text_input.html',
                                                        'input_type': 'color'})

    color_false_negative = serializers.CharField(max_length=7, default="#0000FF",
                                                 help_text='Default: #0000FF, the RGB color used to mark false negatives',
                                                 validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                                 style={'template': 'vadetisweb/parts/input/text_input.html',
                                                        'input_type': 'color',
                                                        'class': 'form-group-last'})

    class Meta:
        model = UserSetting
        fields = ('round_digits', 'color_outliers',
                  'color_true_positive', 'color_false_positive', 'color_false_negative')


class AccountUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='Username', required=True,
                                     min_length=app_settings.USERNAME_MIN_LENGTH,
                                     max_length=get_username_max_length(),
                                     validators=username_validators,
                                     help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                     style={'template': 'vadetisweb/parts/input/text_input.html'})

    first_name = serializers.CharField(label='First Name', required=False,
                                       validators=[alphabetic_validator],
                                       style={'template': 'vadetisweb/parts/input/text_input.html'})

    last_name = serializers.CharField(label='Last Name', required=False,
                                      validators=[alphabetic_validator],
                                      style={'template': 'vadetisweb/parts/input/text_input.html'})

    email = serializers.EmailField(label='E-Mail Address', required=True,
                                   validators=email_validators,
                                   style={'template': 'vadetisweb/parts/input/text_input.html'})

    def validate_email(self, value):
        value = get_account_adapter().clean_email(value)
        errors = {
            "different_account": "This e-mail address is already associated with another account.",
        }
        users = filter_users_by_email(value)
        on_diff_account = [u for u in users if u.pk != self.instance.pk]

        if on_diff_account and app_settings.UNIQUE_EMAIL:
            raise serializers.ValidationError(errors["different_account"])
        return value

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class AccountPasswordSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(label='Current Password', write_only=True, required=True,
                                        allow_null=False, allow_blank=False,
                                        style={'input_type': 'password',
                                               'template': 'vadetisweb/parts/input/text_input.html'})

    password1 = serializers.CharField(label='New Password', write_only=True, required=True,
                                      allow_null=False, allow_blank=False,
                                      style={'input_type': 'password',
                                             'template': 'vadetisweb/parts/input/text_input.html'})

    password2 = serializers.CharField(label='New Password (again)', write_only=True, required=True,
                                      allow_null=False, allow_blank=False,
                                      style={'input_type': 'password',
                                             'template': 'vadetisweb/parts/input/text_input.html'})

    def validate_oldpassword(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Please type your current password.')
        return value

    def validate(self, data):

        # validate password match
        password1 = data['password1']
        password2 = data['password2']
        if (password1 and password2) and password1 != password2:
            raise serializers.ValidationError({'password2': "You must type the same password each time."})

        # validate password
        try:
            # If the password is valid, returns ``None``
            password_validation.validate_password(password1)
        except ValidationError as error:
            raise serializers.ValidationError({'password2': error.messages})

        return data

    def save(self):
        user = self.context['request'].user
        get_account_adapter().set_password(user, self.validated_data["password1"])

    def __init__(self, *args, **kwargs):
        super(AccountPasswordSerializer, self).__init__(*args, **kwargs)


class AccountSocialDisconnectSerializer(serializers.Serializer):
    account = serializers.PrimaryKeyRelatedField(queryset=SocialAccount.objects.none(),
                                                 required=True,
                                                 style={'template': 'vadetisweb/parts/input/select_input.html'})

    def __init__(self, *args, **kwargs):
        super(AccountSocialDisconnectSerializer, self).__init__(*args, **kwargs)


class AccountDeleteSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(initial=True, label='Account is active',
                                         help_text='Uncheck this box and save if you are sure you want to delete your account.',
                                         style={'template': 'vadetisweb/parts/input/checkbox_input.html'})

    class Meta:
        model = User
        fields = ('is_active',)

    def __init__(self, *args, **kwargs):
        super(AccountDeleteSerializer, self).__init__(*args, **kwargs)
