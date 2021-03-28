from django.db import models
from DjangoF1.apps.constructor.models import Constructors
class ConstructorSeason(models.Model):
    constructor = models.ForeignKey(Constructors, on_delete=models.CASCADE, related_name='constructor_season')
    season = models.IntegerField()
    color = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='constructor/logo/' , null = True, blank = True)
    car = models.ImageField(upload_to='constructor/car/', null = True, blank = True)

    def __str__(self):
        return f'{self.constructor} {self.season}'