from django.forms import CharField, PasswordInput, BooleanField, EmailField
from vadetisweb.widgets import IconCheckboxInput, UserTextInput
from allauth.account import app_settings
from allauth.account.forms import LoginForm, ResetPasswordForm, ChangePasswordForm, SetPasswordForm, get_username_max_length, set_form_field_order, filter_users_by_email

from allauth.account.forms import SignupForm as AllauthAccountSignupForm, get_adapter as get_account_adapter
from allauth.socialaccount.forms import SignupForm as AllauthSocialSignupForm, get_adapter as get_socialaccount_adapter

from allauth.socialaccount.forms import DisconnectForm
from allauth.account.utils import logout_on_password_change
from allauth.account.models import EmailAddress

#########################################################
# CUSTOM FIELDS
#########################################################

class AddonPasswordField(CharField):
    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop('render_value', app_settings.PASSWORD_INPUT_RENDER_VALUE)
        kwargs['widget'] = PasswordInput(render_value=render_value,
                                         attrs={'placeholder': kwargs.get('label'),
                                                'class': 'form-control'})
        super(AddonPasswordField, self).__init__(*args, **kwargs)

#########################################################
# ALLAUTH FORM OVERRIDES
#########################################################

class AccountLoginForm(LoginForm):

    password = AddonPasswordField(label="Password")
    remember = BooleanField(widget=IconCheckboxInput(default=True, label='Stay signed in'), required=False, label='Stay signed in')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AccountLoginForm, self).__init__(*args, **kwargs)

        if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
            login_widget = UserTextInput('email', attrs={'type' : 'email',
                                                         'placeholder':  'E-mail address',
                                                         'autofocus': 'autofocus'})
            login_field = EmailField(label='E-mail',
                                     widget=login_widget)

        elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
            login_widget = UserTextInput('username', attrs={'placeholder' : 'Username',
                                                            'autofocus': 'autofocus'})
            login_field = CharField(label='Username',
                                    widget=login_widget,
                                    max_length=get_username_max_length())
        else:
            assert app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME_EMAIL
            login_widget = UserTextInput('username_email', attrs={'placeholder' : 'Username or e-mail',
                                                                  'autofocus': 'autofocus'})
            login_field = CharField(label='Login',
                                    widget=login_widget)

        self.fields["login"] = login_field

        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields['remember']

    def login(self, *args, **kwargs):
        # You can add your own processing here.

        # You must return the original result.
        return super(AccountLoginForm, self).login(*args, **kwargs)