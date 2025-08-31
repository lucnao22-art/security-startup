# file: main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage_view, name="homepage"),
    path("hub/", views.dashboard_hub_view, name="dashboard_hub"),
]
