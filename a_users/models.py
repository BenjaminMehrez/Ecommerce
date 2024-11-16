from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.conf import settings


if settings.ENVIRONMENT == 'production' or settings.POSTGRES_LOCALLY != True:
    from cloudinary.models import CloudinaryField

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    if settings.ENVIRONMENT == 'production' or settings.POSTGRES_LOCALLY != True:
        image = CloudinaryField(null=True, blank=True) # blank signify that can is empty, null can save something empty   
    else:
        image = models.ImageField(upload_to='avatars/', null=True, blank=True) # blank signify that can is empty, null can save something empty   
    full_name = models.CharField(max_length=30, null=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(User, auto_now_add=True)
    
    
    def __str__(self):
        if self.full_name:
            return f'{self.full_name}'
        return self.user.username
        
    
    
    @property
    def name(self):
        if self.full_name:
            return self.full_name
        return self.user.username
    
    
    
    
class ContacUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    
    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
        
        
    def __str__(self):
        return self.full_name