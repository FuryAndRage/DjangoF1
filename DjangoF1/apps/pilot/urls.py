from django.urls import path
from . import views

app_name = 'pilot'

urlpatterns = [
    path('drivers/standing/<str:season>/', views.driver_standing_by_season, name = 'driver_standing_season'),
    path('drivers/<str:season>/',views.drivers_by_season, name='drivers_by_season'),
    path('', views.drivers_current_standing, name = 'current')
    # path('save/pilot/', views.save_pilot, name = 'save'),
    # path('delete/pilot/', views.delete_pilot, name='delete')
]