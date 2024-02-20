from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, NoteVersion


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ShareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class NoteSerializer(serializers.ModelSerializer):
    
    shared_with = ShareUserSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = "__all__"


class NoteVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteVersion
        fields = "__all__"
    
