from django.db import IntegrityError
from rest_framework import serializers

# Phone Number fields
from phonenumber_field.serializerfields import PhoneNumberField

# Password Field Class
class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})
        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True
        super().__init__(*args, **kwargs)

# Models
from apps.user.models import User

# User Profile View/Update
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ( 'id','full_name','contact_number', 'email','photo')
        read_only_fields = ('id', 'email')


# For Add User from admin
class AddUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)
    password = PasswordField(required=True, write_only=True)
    confirm_password = PasswordField(required=True, write_only=True)
    contact_number = PhoneNumberField(required=True)

    class Meta:
        model = User
        fields = ('email', 'contact_number', 'full_name', 'photo', 'password', 'confirm_password', 'is_staff','is_moderator')
        extra_kwargs = {'photo': {'required': False}, 'is_staff': {'required': False} ,'is_moderator': {'required': False} }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        requesting_user = self.context['request'].user
        # Check if the requesting user is an admin
        if requesting_user.is_superuser:
            try:
                return super().create(validated_data)
            except IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e) and ('email' in str(e) or 'contact_number' in str(e)):
                    field = 'email' if 'email' in str(e) else 'contact_number'
                    raise serializers.ValidationError(f'{field.capitalize()} already exists')
                raise e
        else:
            raise serializers.ValidationError("Only admins can create users")


# For Update User Profile
class UpdateDetailUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ( 'id','full_name','contact_number','email','photo','is_staff','is_moderator')
        read_only_fields = ('id', 'email')


# User List Serializer
class UserListSrializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'contact_number')