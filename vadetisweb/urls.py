from django.urls import path
from vadetisweb import views

app_name = 'vadetisweb'

urlpatterns = [
    path('', views.index, name='index'),

]
