from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import update_last_login

# Access Token
from apps.auth_token.service import create_token

# Phone numbers fields
from phonenumber_field.serializerfields import PhoneNumberField

# Import Models
from apps.user.models import User

# Password Field Class
class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})
        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True
        super().__init__(*args, **kwargs)


#Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)
    password = PasswordField(required=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(_('An email address is required to log in.'))

        if password is None:
            raise serializers.ValidationError(_('A password is required to log in.'))

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(_('A user with this email and password was not found.'))

        if not user.is_active:
            raise serializers.ValidationError(_('This user has been deactivated.'))
        
        
        update_last_login(None, user)
        access_token = create_token(user)

        return access_token


# SignUp Serializer
class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True,)
    password = PasswordField(required=True, write_only=True)
    confirm_password = PasswordField(required=True, write_only=True)
    contact_number = PhoneNumberField(required=False)
    
    class Meta:
        model = User
        fields = ('email','contact_number', 'full_name', 'photo', 'password', 'confirm_password',)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e) and ('email' in str(e) or 'contact_number' in str(e)):
                field = 'email' if 'email' in str(e) else 'contact_number'
                raise serializers.ValidationError(f'{field.capitalize()} already exists')
            raise e

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError('Old password is not correct')

        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError('New password cannot be the same as the old password')

        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError('New password and confirm password do not match')

        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
