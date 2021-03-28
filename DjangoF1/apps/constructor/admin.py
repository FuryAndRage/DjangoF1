from django.contrib import admin
from .models import Constructors
from DjangoF1.apps.constructor_season.models import ConstructorSeason

class SeasonInline(admin.TabularInline):
    model = ConstructorSeason
    extra = 0

@admin.register(Constructors)
class ConstructorAdmin(admin.ModelAdmin):
    inlines = (SeasonInline,)
    search_fields = ('constructor_ref','name')
