from django.urls import path
from . import views

app_name = 'pilot'

urlpatterns = [
    path('index/', views.index, name = 'index'),
    path('', views.index, name = 'ind'),
    path('driver/standing/<str:season>/', views.driver_standing_by_season, name = 'driver_standing_season'),
    # path('save/pilot/', views.save_pilot, name = 'save'),
    # path('delete/pilot/', views.delete_pilot, name='delete')
]