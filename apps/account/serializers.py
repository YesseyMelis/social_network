from rest_framework import serializers
from apps.account.models import User


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_login', 'last_activity')
