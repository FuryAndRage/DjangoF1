from django.urls import path
from . import views
app_name = 'season'

urlpatterns = [
    path('<str:season>/', views.season, name  = 'season')
]