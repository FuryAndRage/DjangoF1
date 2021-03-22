from django.db import models

class Pilot(models.Model):
    driver_id = models.IntegerField(null=True)
    driver_ref = models.CharField(max_length=100, null= True)
    number = models.CharField(max_length=10, null = True)
    code = models.CharField(max_length=10, null= True)
    forename = models.CharField(max_length=100, null= True)
    surname = models.CharField(max_length=100, null= True)
    dob = models.DateField(null= True)
    nationality = models.CharField(max_length=255, null= True)
    url = models.URLField(null= True)
    image = models.ImageField(upload_to = 'pilot/', null = True, blank = True)

    class Meta:
        unique_together = ('forename', 'surname')

    def __str__(self):
        return f'{self.forename} {self.surname}'