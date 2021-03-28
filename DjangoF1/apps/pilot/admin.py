from django.contrib import admin

from .models import Pilot

@admin.register(Pilot)
class PilotAdmin(admin.ModelAdmin):
    search_fields = ('driver_id','driver_ref', 'forename', 'surname')
