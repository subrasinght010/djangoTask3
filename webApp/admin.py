from django.contrib import admin

from .models import  Profile, Address, Patient, Doctor,BlogPost,Appointment

# Register your models here.

admin.site.register(Doctor)

admin.site.register(Patient)

admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(BlogPost)
admin.site.register(Appointment)