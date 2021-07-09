from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Perfiles



def profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='guest')
        instance.groups.add(group)
        Perfiles.objects.create(user=instance, email=instance.email, nombre=instance.username )
        User.objects.filter(id=instance.id).update(is_staff=False)

post_save.connect(profile, sender=User)