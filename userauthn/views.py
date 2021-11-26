from Super_Admin.models import Role
from .models import CustomUser
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .utils import Util
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from twilio.rest import Client
import requests
import random
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers, status
from rest_framework.response import Response
from datetime import date
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListCreateAPIView, ListAPIView
from rest_framework import generics
from .serializers import SetNewPasswordSerializer, ForgetPasswordSerializer, SendOtpSerializer, UserLoginSerializer, UserSerializer, ShowuserSerializer, SendOtpSerializer, UserDetailsSerializer
from rest_framework import viewsets
from Super_Admin.models import Role
from Super_Admin.serializers import RoleSerializer

User = get_user_model()
# Create your views here.


class RegisterView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_201_CREATED
            userId = User.objects.filter(username=request.data['username'])
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'User registered  successfully',
                'id': userId[0].id,
                'username': userId[0].username
            }
            return Response(response, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        user = User.objects.filter(
            username=serializer.initial_data['username'])
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User logged in  successfully',
            'userId': serializer.data['username'],
            'username': serializer.initial_data["username"],
            'default_role': user[0].default_role,
            'first_name': serializer.initial_data["username"],
            'username': serializer.initial_data["username"],
            'first_name': user[0].first_name,
            'last_name': user[0].last_name,
        }
        return Response(response, status=status_code)


class SendOTP(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            client = Client(settings.TWILIO_ACCOUNT_SID,
                            settings.TWILIO_AUTH_TOKEN)
            otp = str(random.randint(100000, 999999))
            user_phone_number = serializer.data['country_code'] + \
                serializer.data['phone_number']
            client.messages.create(
                body="Your verification code is "+otp,
                from_="+14104311616",
                to=user_phone_number
            )
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'status code':  status_code,
                'message': 'OTP sent successfully!!',
                'otp': otp,
            }
            return Response(response, status=status_code)
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            'success': 'error',
            'status code':  status_code,
        }
        return Response(response, status=status_code)


@api_view(['POST'])
def editUser(request):
    userid = request.data['user_id']
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    email = request.data['email']
    phone_number = request.data['phone_number']
    CustomUser.objects.filter(id=userid).update(first_name=first_name)
    CustomUser.objects.filter(id=userid).update(last_name=last_name)
    CustomUser.objects.filter(id=userid).update(email=email)
    CustomUser.objects.filter(id=userid).update(phone_number=phone_number)

    try:
        role = request.data['default_role']
        CustomUser.objects.filter(id=userid).update(default_role=role)
    except:
        pass

    status_code = status.HTTP_200_OK
    response = {
        'success': 'True',
        'status code': status_code,
        'message': 'Updated successfully',
    }
    return Response(response, status=status_code)


@api_view(['PUT'])
def updateRole(request, pk):
    try:
        try:
            User.objects.filter(id=pk).update(
                default_role=request.data['default_role'])
        except:
            pass
        
        roles = request.data['userRoles'].split(",")
        user = User.objects.get(id=pk)
        user.role_id.clear()
        for role in roles:
            r = Role.objects.get(role_name=role)
            user.role_id.add(r)
        user.save()

        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Role updated successfully',
        }
    except:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            'success': 'False',
            'status code': status_code,
            'message': 'Some problem occured',
        }
    return Response(response, status=status_code)


@api_view(['DELETE'])
def deleteUser(request, pk):
    # try:
    user = User.objects.get(id=pk)
    print(user.role_id)
    # user.clear()
    # roles = Role.objects.filter(user_id=user.id)
    # try:
    #     for role in roles:
    #         role.user_id.remove(user)
    # except:
    #     pass
    user.delete()
    status_code = status.HTTP_200_OK
    response = {
        'success': 'True',
        'status code': status_code,
        'message': 'User deleted successfully',
    }
    # except:
    #     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    #     response = {
    #         'success': 'False',
    #         'status code': status_code,
    #         'message': 'Some error occured'
    #     }
    return Response(response, status=status_code)


@api_view(['GET'])
def showUser(request, userid):
    # userid = request.data['user_id']
    userdata = CustomUser.objects.filter(id=userid)
    serializer = ShowuserSerializer(userdata, many=True)

    return Response(serializer.data)


class RecoverPassword(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        # data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=request.data)
        email = request.data['recoverEmail']
        # serializer.is_valid(raise_exception=True)
        # return Response({
        #     'success': 'We have sent you a link to reset your password'
        # }, status=status.HTTP_200_OK)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            userIdB64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(request=request).domain
            current_site = 'https://skillbuilderlms-hwr7nalbaq-uc.a.run.app'
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'userIdB64': userIdB64, 'token': token})
            absurl = current_site+relativeLink
            email_body = 'Hello, \n Use below link to reset your password \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Link for reset password'}
            Util.send_mail(data)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'We have sent you a link to reset password',
            'status_code': status_code
        }
        return HttpResponse(response, status=status_code)


class PasswordTokenCheckAPI(GenericAPIView):
    def get(self, request, userIdB64, token):
        try:
            userId = smart_str(urlsafe_base64_decode(userIdB64))
            user = User.objects.get(id=userId)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                'success:': True,
                'message': 'Credentials Valid',
                'userIdB64': userIdB64,
                'token': token
            }, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPI(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'success': True,
            'message': 'Password Reset Successful',
        }, status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserDetails(ListAPIView):
    queryset = User.objects.all()
    serializerClass = UserDetailsSerializer

    def get(self, requesy, pk):
        self.queryset = User.objects.get(id=pk)
        serializer = self.serializerClass(self.queryset, many=False)
        return Response(serializer.data)


class AllRolesDetails(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    serializerClass = RoleSerializer

    def get_queryset(self):
        role = Role.objects.all()
        # self.queryset = User.objects.get(id=pk)
        # serializer = self.serializerClass(self.queryset, many=False)
        return role
