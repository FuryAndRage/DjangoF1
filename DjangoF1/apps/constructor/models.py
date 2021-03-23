from django.db import models

class Constructors(models.Model):
    constructor_id = models.IntegerField()
    constructor_ref = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    url = models.URLField()
    image = models.ImageField(upload_to = 'constructor/', null = True, blank = True)


    def __str__(self):
        return self.name