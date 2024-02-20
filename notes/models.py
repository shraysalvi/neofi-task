from django.db import models
from django.contrib.auth.models import User

 
class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shared_with = models.ManyToManyField(User, related_name="notes", through='SharedNote', blank=True)


class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class NoteVersion(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)
    version_number = models.PositiveIntegerField()
    # changes = models.TextField()
