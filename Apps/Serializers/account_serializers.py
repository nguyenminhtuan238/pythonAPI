from rest_framework import serializers
import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password','email']
        
    def validate_password(self, value):
        # Kiểm tra độ dài mật khẩu
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        # Kiểm tra xem mật khẩu có chứa cả chữ và số không
        if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
            raise serializers.ValidationError("Password must contain at least one letter and one number.")

        return value
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email cannot be empty.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Invalid email format.")

        return value
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['email']
        validated_data['password'] = make_password(password)
        account = User.objects.create(**validated_data)        
        return account  