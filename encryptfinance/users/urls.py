from __future__ import absolute_import

from django.urls import path

from encryptfinance.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    # user_profile_view,
    user_verify_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<str:username>/verify/", view=user_verify_view, name="verify"),
    # path("<str:username>/profile/", view=user_profile_view, name="profile"),
]
