from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.models import User


class UserRegiserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_email(self, email):
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("This email address is already in use.")
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def validate_password_strong(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least 1 digit.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least 1 letter.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least 1 uppercase letter.")
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least 1 lowercase letter.")
        return password

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Those passwords don't match.")
        self.validate_password_strong(password)
        return data
