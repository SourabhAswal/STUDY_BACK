from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed
from Super_Admin.models import Role
from Super_Admin.serializers import RoleSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)
    phone_number = serializers.CharField(max_length=10)
    default_role = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'phone_number', 'default_role', 'role_id']
        depth = 1

    def validate(self, attrs):
        email = attrs.get('email', '')
        phone = attrs.get('phone_number', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'status': 'Email is already in use'})
        if User.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError(
                {'status': 'phone number is already in use'})
        return super().validate(attrs)

    def create(self, validaate_data):
        return User.objects.create_user(**validaate_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        # print(user)
        if user is None:
            raise serializers.ValidationError({'status': 'A user with this email and password is not found.'
                                               })
        try:
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError({'status': 'User with given email and password does not exists'
                                               })
        return {
            'username': user.id,
            
        }


class SendOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=14)
    country_code = serializers.CharField()

    class Meta:
        model = User
        fields = ['phone_number']

    def validate(self, attrs):
        phone = attrs.get('phone_number', '')
        countryCode = attrs.get('country_code', '')
        if User.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError(
                {'status': 'phone number is already in use'})
        return super().validate(attrs)


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=4)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs['data'].get('recoverEmail', '')

        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    userIdB64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'userIdB64', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password', '')
            confirm_password = attrs.get('confirmPassword', '')
            token = attrs.get('token', '')
            userIdB64 = attrs.get('userIdB64', '')
            id = urlsafe_base64_decode(userIdB64)
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            # elif password == confirm_password:
            user.set_password(password)
            user.save()
            return user

            # raise AuthenticationFailed("Password and confirm password are different")

        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)

        return super().validate(attrs)


class ShowuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'default_role', 'role_id']
        depth = 1


class AllUsersSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone_number', 'default_role', 'role_id']
        depth = 1


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone_number', 'default_role', 'role_id']
