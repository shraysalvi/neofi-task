from django.urls import path
from notes.views import NoteView, get_update_note, share_note, NoteVersionViewSet


urlpatterns = [
    path('create/', NoteView.as_view(), name='create_note'),
    path('<int:id>/', get_update_note, name='get_update_note'),
    path('<int:note_id>/share/', share_note, name='share_note'),
    path('version-history/<int:note_id>/', NoteVersionViewSet.as_view(), name='version_history'),
]
