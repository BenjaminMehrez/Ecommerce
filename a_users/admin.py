from django.contrib import admin
from .models import *


# Register your models here.


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']




admin.site.register(Profile)
admin.site.register(ContacUs, ContactUsAdmin)