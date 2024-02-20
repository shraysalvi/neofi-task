from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Note, NoteVersion


@receiver(post_save, sender=Note)
def save_profile(signal, instance, created, **kwargs):
    if created:
        NoteVersion.objects.create(note=instance, editor=instance.owner, version_number=1)
