from django.contrib import admin
from .models import Pilot
from DjangoF1.apps.pilot_season.models import PilotSeason

class PilotSeasonInline(admin.TabularInline):
    model = PilotSeason
    extra = 0
@admin.register(Pilot)
class PilotAdmin(admin.ModelAdmin):
    inlines = (PilotSeasonInline,)
    search_fields = ('driver_id','driver_ref', 'forename', 'surname')
