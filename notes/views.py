from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignUpSerializer, NoteSerializer, NoteVersionSerializer
from rest_framework import permissions
from .models import Note, NoteVersion
from rest_framework.decorators import api_view
from rest_framework import generics


class NoteVersionViewSet(generics.ListAPIView):

    model=NoteVersion
    serializer_class = NoteVersionSerializer

    def get_queryset(self, id):
        return NoteVersion.objects.filter(note__pk=id)

    def list(self, request, note_id):
        queryset = self.get_queryset(note_id)
        serializer = NoteVersionSerializer(queryset, many=True)
        return Response(serializer.data)


class UserSignup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteView(APIView):
    def post(self, request):
        data = request.data
        data['owner'] = request.user.pk

        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_note_version(note, editor):
    """Create a new version of the note when it is updated."""

    nv = NoteVersion.objects.filter(note=note)
    if nv.exists():
        prev_version = nv.latest('version_number').version_number
    else:
        prev_version = 0
    NoteVersion.objects.create(note=note, editor=editor, version_number=prev_version+1)


def check_note_permission(id, user):
    """Check if the user has permission to access the note."""

    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        return Response({"error": ["Note not found"]}, status=status.HTTP_404_NOT_FOUND)
    
    if note.owner != user and (user not in note.shared_with.all()):
        return Response({"error": ["Permission denied"]}, status=status.HTTP_403_FORBIDDEN)
    
    return note


@api_view(['GET', 'PUT'])
def get_update_note(request, id):

    note = check_note_permission(id, request.user)

    if isinstance(note, Response):
        return note

    if request.method == 'GET':
        return Response(NoteSerializer(note).data)

    elif request.method == 'PUT':
        content = request.data.get('content')
        if content is None:
            return Response({"error":["content note provided"]}, status=status.HTTP_400_BAD_REQUEST)
        create_note_version(note, request.user)
        note.content = content
        note.save()
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def share_note(request, note_id):
    """Share a note."""

    note = check_note_permission(note_id, request.user)
    
    if isinstance(note, Response):
        return note
    
    # Check for the shared_with
    share_with = request.data.get('shared_with')
    if share_with is not None:
        try:
            note.shared_with.set(share_with)
        except Exception as e:
            return Response({"error":[str(e)]}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"success": "Note shared with the given users"}, status=status.HTTP_201_CREATED)
