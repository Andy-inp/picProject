from django.urls import path, re_path
from . import views

app_name = 'smmsmanage'

urlpatterns = [
    path('upload/', views.upload, name='smmsmanage'),
    path('img-list/', views.img_list, name='img_list'),
    path('img-list/singeldel', views.delimg, name='delimg'),
    path('img-list/batchdel', views.batchdelimg, name='batchdelimg'),
    # path('img-list/<int:imglist>/', views.imglist_json, name='imglist_json'),
    re_path(r'^img-list/(?P<imglist>\w+).json', views.imglist_json, name='imglist_json'),
]
