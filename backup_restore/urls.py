# file: backup_restore/urls.py
from django.urls import path
from . import views

app_name = "backup_restore"
urlpatterns = [
    path("", views.backup_restore_view, name="main"),
]
