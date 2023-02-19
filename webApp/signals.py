from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Doctor, Patient, Address


@receiver(post_save, sender=User, dispatch_uid="create_profile_and_associated_models")
def create_profile_and_associated_models(sender, instance, created, **kwargs):
    if created:
        profile, _ = Profile.objects.get_or_create(user=instance)
        user_type = profile.user_type
        if user_type == "doctor":
            Doctor.objects.get_or_create(user=instance)
        elif user_type == "patient":
            Patient.objects.get_or_create(user=instance)
        
        address, created = Address.objects.get_or_create()


@receiver(post_save, sender=User, dispatch_uid="save_profile_and_associated_models")
def save_profile_and_associated_models(sender, instance, **kwargs):
    try:
        instance.profile.save()
        user_type = instance.profile.user_type
        if user_type == "doctor":
            instance.doctor.save()
        elif user_type == "patient":
            instance.patient.save()
    except Profile.DoesNotExist:
        pass
    
    try:
        instance.address.save()
    except Address.DoesNotExist:
        pass
