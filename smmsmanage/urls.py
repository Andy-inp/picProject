from django.urls import path
from . import views

app_name = 'smmsmanage'

urlpatterns = [
    path('upload/', views.upload, name='smmsmanage'),
    path('img-list/', views.img_list, name='smmsmanage'),
]
