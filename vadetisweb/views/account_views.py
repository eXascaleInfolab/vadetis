from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from vadetisweb.forms.account_forms import *
from vadetisweb.utils import cookie_settings_dict
from vadetisweb.models import UserSettings

#########################################################
# Account Views
#########################################################

@login_required
def account(request):
    current_user = request.user

    form_password = None
    form_account_delete = None
    form_social_disconnect = None
    form_user = None

    if request.method == 'POST':

        # check which form was submitted
        if 'submit-user' in request.POST:
            form_user = AccountUserForm(instance=current_user, data=request.POST)
            if form_user.is_valid():
                user = form_user.save()
                message = "Your account has been updated!"
                messages.success(request, message)
            else:
                print(form_user.errors)

        elif 'submit-password' in request.POST:

            if not request.user.has_usable_password():
                form_password = AccountSetPasswordForm(user=current_user, data=request.POST)
                message = "Your password has been set!"
            else:
                form_password = AccountChangePasswordForm(user=current_user, data=request.POST)
                message = "Your password has been updated!"

            if form_password.is_valid():
                form_password.save()
                update_session_auth_hash(request, form_password.user)
                messages.success(request, message)
                form_password = AccountChangePasswordForm(user=current_user)
            else:
                message = "Could not update password!"
                messages.error(request, message)

        elif 'submit-social-account-disconnect' in request.POST:
            form_social_disconnect = AccountSocialDisconnectForm(request=request, data=request.POST)
            if form_social_disconnect.is_valid():
                form_social_disconnect.save()
                messages.success(request, "Social account has been disconnected from your Vadetis account!")
                form_social_disconnect = AccountSocialDisconnectForm(request=request)
            else:
                message = "Could not disconnect social account!"
                messages.error(request, message)
                print(form_social_disconnect.errors)

        elif 'submit-account-delete' in request.POST:
            form_account_delete = AccountDeleteUserForm(instance=current_user, data=request.POST)
            if form_account_delete.is_valid():

                deactivate_user = form_account_delete.save()

                # check if user no longer active, then delete
                # remove this if you want only to deactivate
                if deactivate_user.is_active == False:
                    deactivate_user.delete()
                    message = "Account has been removed"
                    messages.success(request, message)
                    return HttpResponseRedirect(reverse_lazy('account_logout'))

    if form_user is None:
        form_user = AccountUserForm(instance=current_user)

    if form_password is None and not request.user.has_usable_password():
        form_password = AccountSetPasswordForm(user=current_user)
    elif form_password is None:
        form_password = AccountChangePasswordForm(user=current_user)

    if form_social_disconnect is None:
        form_social_disconnect = AccountSocialDisconnectForm(request=request)

    if form_account_delete is None:
        form_account_delete = AccountDeleteUserForm(instance=current_user)

    url_social_connect_success_redirect = reverse('vadetisweb:account')

    response = render(request, 'vadetisweb/account/account.html', {'form_user' : form_user,
                                                                   'form_password':form_password,
                                                                   'form_social_disconnect' : form_social_disconnect,
                                                                   'form_account_delete':form_account_delete,
                                                                   'url_social_connect_success_redirect' : url_social_connect_success_redirect
                                                                   })
    return response


def application_settings(request):
    user = request.user
    settings_dict = cookie_settings_dict(request)
    updateCookies = False

    if user.is_authenticated: #use profile

        settings, created = UserSettings.objects.get_or_create(user=user)
        if created:
            # fill profile with values from cookies
            # (e.g. user used app, then later made an account-> values from cookies should be inserted into profile)
            for (key, value) in settings_dict.items():
                setattr(settings, key, value)
            settings.save()

        if request.method == 'POST':
            form = UserSettingsForm(instance=settings, data=request.POST)

            if form.is_valid():
                user_settings = form.save(commit=False)
                user_settings.user = user

                user_settings.save()

                message = "Your settings have been updated!"
                messages.success(request, message)

                updateCookies = True
            else:
                message = "Settings could not be saved! Check for form errors below."
                messages.error(request, message)

        else:
            form = UserSettingsForm(instance=settings)

    else:   #use cookie
        temp_settings = UserSettings(**settings_dict)

        if request.method == 'POST':
            form = UserSettingsForm(instance=temp_settings, data=request.POST)

            if form.is_valid():
                #set cookies

                message = "Your settings have been updated!"
                messages.success(request, message)

                updateCookies = True

            else:
                message = "Settings could not be saved! Check for form errors below."
                messages.error(request, message)

        else:
            form = UserSettingsForm(instance=temp_settings)

    response = render(request, 'vadetisweb/account/application_settings.html', {'form' : form, })

    #set cookies for response
    if updateCookies:
        for key in settings_dict.keys():
            response.set_cookie(key=key, value=form.cleaned_data[key])

    return response