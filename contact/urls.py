from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('identify/', views.IdentifyAPIView.as_view(), name='identify'),
    path('contactdetails/', views.Contactdetails.as_view(), name='contactdetails'),
]