from django.urls import path
from vadetisweb import views

urlpatterns = [
    path('', views.index, name='index'),

]
