from django.contrib import admin
from .models import Note, SharedNote, NoteVersion
from django.contrib.sessions.models import Session


class NoteAdmin(admin.ModelAdmin):
    list_display = ("owner", "content")

admin.site.register(Note, NoteAdmin)

admin.site.register(SharedNote)

class NoteVersionAdmin(admin.ModelAdmin):
    list_display = ("note", "editor", "version_number")

admin.site.register(NoteVersion, NoteVersionAdmin)

class SessionAdmin(admin.ModelAdmin):

    list_display = ("session_key", "expire_date")
    list_filter = ("expire_date", )
    list_per_page = 100

admin.site.register(Session, SessionAdmin)
