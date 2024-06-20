from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path("identify/", views.ContactView.as_view(), name='identify'),
]