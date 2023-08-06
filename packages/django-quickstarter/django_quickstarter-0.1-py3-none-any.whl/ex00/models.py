from django.db import models

class Photo(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.TextField(null=False)

    def __str__(self):
        return self.title