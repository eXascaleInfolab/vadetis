from allauth.account import app_settings
from allauth.account.forms import LoginForm, ResetPasswordForm, ChangePasswordForm, SetPasswordForm, ResetPasswordKeyForm, get_username_max_length, \
    set_form_field_order, SignupForm as AllauthAccountSignupForm
from captcha.fields import ReCaptchaField
from django.forms import CharField, PasswordInput, BooleanField, EmailField
from django.conf import settings

from vadetisweb.widgets import FormCheckboxInput, UserTextInput


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
# Account Forms & Registration
#########################################################

class AccountLoginForm(LoginForm):

    password = AddonPasswordField(label="Password")
    remember = BooleanField(widget=FormCheckboxInput(default=True, label='Stay signed in'), required=False, label='Stay signed in')

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
        
        if not settings.DEBUG:
            self.fields["captcha"] = ReCaptchaField(label="")

        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields['remember']

    def login(self, *args, **kwargs):
        # You can add your own processing here.

        # You must return the original result.
        return super(AccountLoginForm, self).login(*args, **kwargs)


class AccountSignUpForm(AllauthAccountSignupForm):

    username = CharField(label='Username',
                               min_length=app_settings.USERNAME_MIN_LENGTH,
                               widget=UserTextInput('username', attrs={'placeholder' : 'Username',
                                                                       'autofocus': 'autofocus'}))
    email = EmailField(widget=UserTextInput('email', attrs={'type' : 'email',
                                                            'placeholder':  'E-mail address',
                                                            'autofocus': 'autofocus'}))

    def __init__(self, *args, **kwargs):
        super(AccountSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = AddonPasswordField(label='Password')
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields['password2'] = AddonPasswordField(label='Password (again)')
            self.field_order =  ['username', 'email', 'password1', 'password2', 'captcha']
        else:
            self.field_order = ['username', 'email', 'password1', 'captcha']

        if hasattr(self, 'field_order'):
            set_form_field_order(self, self.field_order)
            
        if not settings.DEBUG:
            self.fields["captcha"] = ReCaptchaField(label="")


class AccountResetPasswordForm(ResetPasswordForm):

    email = EmailField(label='E-mail', required=True, widget=UserTextInput('email', attrs={'type' : 'email',
                                                                                           'size' : '30',
                                                                                           'placeholder': 'E-mail address',}))
    #captcha = ReCaptchaField(label="")

    def __init__(self, *args, **kwargs):
        super(AccountResetPasswordForm, self).__init__(*args, **kwargs)

        if not settings.DEBUG:
            self.fields["captcha"] = ReCaptchaField(label="")


class AccountChangePasswordForm(ChangePasswordForm):

    def __init__(self, user=None, *args, **kwargs):
        super(AccountChangePasswordForm, self).__init__(user, *args, **kwargs)
        for field in ('oldpassword', 'password1', 'password2'):
            self.fields[field].widget.attrs = {'class': 'form-control'}

    def save(self):
        # Ensure you call the parent classes save
        # .save() does not return anything
        super(AccountChangePasswordForm, self).save()


class AccountResetPasswordKeyForm(ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super(AccountResetPasswordKeyForm, self).__init__(*args, **kwargs)
        for field in ('password1', 'password2'):
            self.fields[field].widget.attrs = {'class': 'form-control'}

    def save(self):
        super(AccountResetPasswordKeyForm, self).save()


class AccountSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(AccountSetPasswordForm, self).__init__(*args, **kwargs)
        for field in ('password1', 'password2'):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self):
        # Ensure you call the parent classes save
        # .save() does not return anything
        super(AccountSetPasswordForm, self).save()
