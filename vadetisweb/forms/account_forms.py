from allauth.account import app_settings
from allauth.account.forms import get_adapter as get_account_adapter, SetPasswordForm, filter_users_by_email
from allauth.account.models import EmailAddress
from django.forms import ModelForm, ValidationError

from vadetisweb.models import User


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
