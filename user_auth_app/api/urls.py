from django.contrib import admin
from django.urls import path
from .views import registration_view, login_view, email_check_view

urlpatterns = [
    path('registration/', registration_view),
    path('login/', login_view),
    path('email-check/', email_check_view)
]
