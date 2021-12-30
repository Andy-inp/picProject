from django.urls import path, re_path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('home/', views.home, name='home'),
    # path('home/<int:id>/', views.home, name='home'),
    re_path('^usage-overview/', views.usage_overview, name='usage_overview'),
]
