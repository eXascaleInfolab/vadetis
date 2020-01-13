from django.forms import ModelForm, ValidationError
from vadetisweb.models import User
from allauth.account import app_settings
from allauth.account.models import EmailAddress
from allauth.account.forms import SignupForm as AllauthAccountSignupForm, get_adapter as get_account_adapter, LoginForm, ResetPasswordForm, ChangePasswordForm, SetPasswordForm, get_username_max_length, set_form_field_order, filter_users_by_email
from allauth.socialaccount.forms import SignupForm as AllauthSocialSignupForm, DisconnectForm

from vadetisweb.models import UserSettings
from vadetisweb.widgets import ColorPickerTextInput

#########################################################
# Account Forms
#########################################################

class AccountUserForm(ModelForm):
    """
    The form for the user basic config
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(AccountUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        setattr(self, '__original_email', self.instance.email)

    def valid_email(self):
        value = self.instance.email
        value = get_account_adapter().clean_email(value)
        errors = {
            "different_account": "This e-mail address is already associated with another account.",
        }
        users = filter_users_by_email(value)
        on_diff_account = [u for u in users if u.pk != self.user.pk]

        if on_diff_account and app_settings.UNIQUE_EMAIL:
            raise ValidationError(errors["different_account"])
        return value

    def save(self, commit=True):
        instance = super(AccountUserForm, self).save(commit=False)

        email_address = EmailAddress.objects.get(email__iexact=getattr(self, '__original_email'), user=self.instance)
        if email_address is not None:
            email_address.email = self.cleaned_data['email']
            email_address.save()
        else:
            raise ValidationError('Something went wrong, could not set email address')
        if commit:
            instance.save()
        return instance


class AccountSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(AccountSetPasswordForm, self).__init__(*args, **kwargs)
        for field in ('password1', 'password2'):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self):
        # Ensure you call the parent classes save
        # .save() does not return anything
        super(AccountSetPasswordForm, self).save()


class AccountChangePasswordForm(ChangePasswordForm):

    def __init__(self, user=None, *args, **kwargs):
        super(AccountChangePasswordForm, self).__init__(user, *args, **kwargs)
        for field in ('oldpassword', 'password1', 'password2'):
            self.fields[field].widget.attrs = {'class': 'form-control'}

    def save(self):
        # Ensure you call the parent classes save
        # .save() does not return anything
        super(AccountChangePasswordForm, self).save()


class AccountSocialDisconnectForm(DisconnectForm):

    def save(self):

        # Add your own processing here if you do need access to the
        # socialaccount being deleted.

        # Ensure you call the parent classes save.
        # .save() does not return anything
        super(AccountSocialDisconnectForm, self).save()

        # Add your own processing here if you don't need access to the
        # socialaccount being deleted.


class AccountDeleteUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super(AccountDeleteUserForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = 'Uncheck this box if you are sure you want to delete your account.'


class UserSettingsForm(ModelForm):
    """
    The form for the settings of the user
    """
    #group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = UserSettings
        fields = ('highcharts_height', 'legend_height', 'color_outliers', 'color_clusters',
                  'color_true_positive', 'color_false_positive', 'color_false_negative', 'round_digits')
        widgets = {
            'color_outliers' : ColorPickerTextInput,
            'color_clusters' : ColorPickerTextInput,
            'color_true_positive' : ColorPickerTextInput,
            'color_false_positive' : ColorPickerTextInput,
            'color_false_negative' : ColorPickerTextInput,
        }

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        for field in ('highcharts_height', 'legend_height', 'round_digits'):
            self.fields[field].widget.attrs = {'class': 'form-control'}