from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('usage-overview/', views.usage_overview, name='usage_overview'),
]
