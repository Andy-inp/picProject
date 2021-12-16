from django.urls import path
from . import views

app_name = 'homeapp'

urlpatterns = [
    path('login/', views.user_login, name='user_login'),

    #path('home/', views.home, name='home'),
]
