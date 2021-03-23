from django.urls import path
from . import views

app_name = 'pilot'

urlpatterns = [
    path('index/', views.index, name = 'index'),
    path('', views.index, name = 'save')
]