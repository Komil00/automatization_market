from rest_framework import serializers

from users.models import *
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = "__all__"

    def create(self, validated_data):
        return Director.objects.create_user(username=validated_data['username'], password=validated_data['password'])


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = "__all__"

    def create(self, validated_data):
        return Manager.objects.create_user(username=validated_data['username'], password=validated_data['password'])


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=223, required=True)
    password = serializers.CharField(max_length=68, write_only=True)
    first_name = serializers.CharField(max_length=223, read_only=True)
    last_name = serializers.CharField(max_length=223, read_only=True)

    def get_fist_name(self, obj):
        username = obj.get('username')
        user = User.objects.filter(username=username).first()
        return user.first_name

    def get_last_name(self, obj):
        username = obj.get('username')
        user = User.objects.filter(username=username).first()
        return user.last_name

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed({
                "status": False,
                "message": "Username or password is not correct"
            })

        data = {
            "success": True,
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        refresh = RefreshToken.for_user(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class IshchiSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ishchi
        fields = [
            'id',
            'ism_sharif',
            'lavozim',
            'telefon',
            'vaqt',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['count'] = Ishchi.objects.count()
        return representation


