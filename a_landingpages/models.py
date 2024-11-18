from django.db import models

# Create your models here.


class LandingPage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_enabled = models.BooleanField(default=False)
    access_code = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['name']