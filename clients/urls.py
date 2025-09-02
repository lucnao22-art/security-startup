# file: clients/urls.py
from django.urls import path
from . import views

app_name = "clients"
urlpatterns = [
    path("pipeline/", views.pipeline_view, name="pipeline"),
    path("dashboard/", views.kinh_doanh_dashboard_view, name="dashboard-kinh-doanh"),
]
