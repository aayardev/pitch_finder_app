from django.urls import path
from .views import (
    pitch_list_api_view,
    reservation_create_api_view,
    signup_view,
    login_view,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("pitches/", pitch_list_api_view, name="pitch-list"),
    path(
        "reservations/",
        reservation_create_api_view,
        name="reservation-create",
    ),
]
