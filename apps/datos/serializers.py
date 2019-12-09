import hashlib

from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers

from apps.utils.print_colors import _green, _blue
from apps.utils.shortcuts import get_object_or_none
from .models import Transaction, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'birth_date',
        )

    @transaction.atomic
    def create(self, validated_data):
        print(_green(validated_data))
        email = validated_data['email']
        user = get_object_or_none(CustomUser, email=validated_data['email'])
        if not user:
            validated_data['id'] = hashlib.md5(email.encode('utf-8')).hexdigest()
            validated_data['password'] = make_password(validated_data['password'])
            print(_blue(validated_data))
            return super().create(validated_data)
        raise serializers.ValidationError({'error': 'user already exist'})


class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

