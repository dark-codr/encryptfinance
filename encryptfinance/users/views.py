from __future__ import absolute_import

import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect


from .models import UserVerify, UserProfile
from .forms import UserProfileForm, UserVerifyForm, UserPersonalForm
User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["crypto"] = get_crypto_data()
    #     return context
    


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserProfile
    form_class = UserProfileForm
    # second_form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_message = _("Your personal information was successfully updated")
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        self.user = self.request.user
        return super().get_object()

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(UserProfile, user__username__iexact=username)

    def get(self, request, *args, **kwargs):
        self.user = request.user
        return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["profileform"] = self.form_class(self.request.POST, self.request.FILES, instance=self.request.user)
    #     return context
    

    def form_valid(self, form):
        form.save()
        time = timezone.now()
        userdata = self.request.user
        title = "User Data Update"
        msg = f"{userdata.username} just updated his personal details at {time}"
        message = get_template('mail/admin-mail.html').render(context={"user_username": userdata.username, "title": title, "time": time, "message": msg})
        recepient = str(userdata.email)
        frm = settings.EMAIL_HOST_USER
        mail = EmailMessage(
                    title, 
                    #f"{self.request.user.username} just updated his profile at {self.created}", 
                    message,
                    frm, 
                    [recepient], 
                )
        mail.content_subtype = "html"
        mail.send()
        return super().form_valid(form)

    def form_invalid(self, form):
        return messages.error(self.request, "Form was not submited successfully. Check your informations!")
user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserVerifyCreateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserVerify
    form_class = UserVerifyForm
    template_name = 'users/verify.html'
    slug_field = "username"
    slug_url_kwarg = "username"
    success_message = _("Verification information was successfully created")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(UserVerify, user__username__iexact=username)

    def get(self, request, *args, **kwargs):
        self.user = request.user
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        time = timezone.now()
        title = "New Verification Request"
        msg = f"{self.request.user.username} just submited informations for his profile verification at {time}"
        message = get_template('mail/admin-mail.html').render(context={"user_username": self.request.user.username, "title": title, "time": time, "message": msg})
        recepient = self.request.user.email
        sender = settings.EMAIL_HOST_USER
        mail = EmailMessage(
            title, 
            message, 
            sender, 
            [recepient]
        )
        mail.content_subtype = "html"
        mail.send()

        return super().form_valid(form)

    def form_invalid(self, form):
        return messages.error(self.request, "Form was not submited successfully. Check your informations!")

user_verify_view = UserVerifyCreateView.as_view()
