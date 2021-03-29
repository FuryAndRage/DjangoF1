from django.db import models
from DjangoF1.apps.pilot.models import Pilot
class PilotSeason(models.Model):
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE, related_name='pilot_season')
    season = models.IntegerField()
    image = models.ImageField(upload_to = 'pilot/season_image/', null = True, blank = True)

    def __str__(self):
        return str(self.pilot)
